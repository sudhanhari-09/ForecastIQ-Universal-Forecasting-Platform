import os, csv, io, json
from flask import (Blueprint, render_template, request,
                   redirect, url_for, flash, session, send_file, Response)
from routes.auth import login_required
from services.dataset_service import get_dataset
from services.forecasting_service import (
    run_automatic_forecasting, run_manual_forecasting,
    get_forecast_report, load_forecast_results,
    ALL_MODELS, TRADITIONAL_MODELS, ML_MODELS, DL_MODELS,
    _is_numeric_timestamp
)
from services.datetime_utils import detect_date_columns as shared_detect_dates
from services.activity_service import log_activity
from services.workflow_service import get_workflow_state, get_step_urls as wf_get_step_urls, require_step_completion, complete_step
from services.dataset_service import read_dataframe
from models.preprocessing_report_model import PreprocessingReport
import pandas as pd
import numpy as np

forecasting_bp = Blueprint('forecasting', __name__)


def _get_column_info(dataset_id, user_id):
    dataset = get_dataset(dataset_id, user_id)
    if not dataset:
        return None, None, None, None

    prep = PreprocessingReport.query.filter_by(dataset_id=dataset_id).order_by(
        PreprocessingReport.created_at.desc()
    ).first()
    if prep and prep.output_file and os.path.exists(prep.output_file):
        file_path = prep.output_file
        ext = 'csv'
    else:
        file_path = dataset.file_path
        ext = dataset.file_name.rsplit('.', 1)[1].lower()

    if ext == 'csv':
        df = read_dataframe(file_path, 'csv')
    else:
        df = read_dataframe(file_path, ext)

    if df is None:
        return None, None, None, None

    numeric = list(df.select_dtypes(include=['number']).columns)
    categorical = list(df.select_dtypes(include=['object', 'category']).columns)
    date_cols = shared_detect_dates(df)
    for col in df.columns:
        if str(col) not in date_cols and _is_numeric_timestamp(df[col]):
            date_cols.append(str(col))
    return numeric, categorical, date_cols, df.columns.tolist()


def _validate_forecast_results(results_data, dataset_id):
    if not results_data:
        return False, 'No forecast results found.'
    valid = results_data.get('validation', {})
    if not valid:
        return False, 'Validation metadata missing.'
    fields = ['dataset_id', 'forecast_id', 'model', 'testing_count', 'future_count']
    for f in fields:
        if f not in valid:
            return False, f'Validation field "{f}" missing.'
    if valid.get('dataset_id') != dataset_id:
        return False, f'Dataset ID mismatch: expected {dataset_id}, got {valid.get("dataset_id")}'
    return True, None


@forecasting_bp.route('/forecasting/<int:dataset_id>')
@login_required
def mode_selection(dataset_id):
    dataset = get_dataset(dataset_id, session['user_id'])
    if not dataset:
        flash('Dataset not found.', 'danger')
        return redirect(url_for('dataset.list_datasets'))
    resp = require_step_completion(dataset_id, 5)
    if resp:
        return resp
    return redirect(url_for('forecasting.setup', dataset_id=dataset_id))


@forecasting_bp.route('/forecasting/setup/<int:dataset_id>')
@login_required
def setup(dataset_id):
    dataset = get_dataset(dataset_id, session['user_id'])
    if not dataset:
        flash('Dataset not found.', 'danger')
        return redirect(url_for('dataset.list_datasets'))
    resp = require_step_completion(dataset_id, 5)
    if resp:
        return resp

    numeric, categorical, date_cols, all_cols = _get_column_info(dataset_id, session['user_id'])
    if numeric is None:
        flash('Unable to read dataset.', 'danger')
        return redirect(url_for('dataset.list_datasets'))

    workflow_state = get_workflow_state(dataset_id)
    step_urls = wf_get_step_urls(dataset_id, 5, workflow_state)
    return render_template('forecast_setup.html', dataset=dataset,
                           numeric_columns=numeric, date_columns=date_cols,
                           all_columns=all_cols,
                           traditional_models=list(TRADITIONAL_MODELS.keys()),
                           ml_models=list(ML_MODELS.keys()),
                           dl_models=list(DL_MODELS.keys()),
                           all_models=list(ALL_MODELS.keys()),
                           dataset_id=dataset_id,
                           current_step=workflow_state['current'],
                           workflow_state=workflow_state, step_urls=step_urls)


@forecasting_bp.route('/forecasting/train/<int:dataset_id>', methods=['POST'])
@login_required
def train(dataset_id):
    dataset = get_dataset(dataset_id, session['user_id'])
    if not dataset:
        flash('Dataset not found.', 'danger')
        return redirect(url_for('dataset.list_datasets'))
    resp = require_step_completion(dataset_id, 5)
    if resp:
        return resp

    horizon = request.form.get('horizon', 30, type=int)
    test_ratio_str = request.form.get('test_ratio', '0.2')
    test_ratio = float(test_ratio_str) if test_ratio_str else 0.2
    target_col = request.form.get('target_column', '')
    date_col = request.form.get('date_column', '')
    model_name = request.form.get('model_name', '')

    if model_name:
        if not target_col:
            flash('Please select a target column.', 'warning')
            return redirect(url_for('forecasting.setup', dataset_id=dataset_id))
        if not date_col:
            flash('Please select a date column.', 'warning')
            return redirect(url_for('forecasting.setup', dataset_id=dataset_id))
        results, error = run_manual_forecasting(
            dataset_id, session['user_id'],
            target_col=target_col, date_col=date_col,
            model_name=model_name,
            horizon=horizon, test_ratio=test_ratio
        )
        log_type = 'forecast_manual_completed'
    else:
        results, error = run_automatic_forecasting(
            dataset_id, session['user_id'], horizon=horizon,
            test_ratio=test_ratio, target_col=target_col or None
        )
        log_type = 'forecast_auto_completed'

    if error:
        flash(error, 'danger')
        return redirect(url_for('forecasting.setup', dataset_id=dataset_id))

    log_activity(session['user_id'], log_type, 'forecasting', dataset_id,
                 f'Forecasting completed for {dataset.file_name}')
    flash('Forecasting completed successfully!', 'success')
    complete_step(dataset_id)
    return redirect(url_for('forecasting.results', dataset_id=dataset_id))


@forecasting_bp.route('/forecasting/results/<int:dataset_id>')
@login_required
def results(dataset_id):
    dataset = get_dataset(dataset_id, session['user_id'])
    if not dataset:
        flash('Dataset not found.', 'danger')
        return redirect(url_for('dataset.list_datasets'))
    resp = require_step_completion(dataset_id, 5)
    if resp:
        return resp

    results_data = load_forecast_results(dataset_id)
    if not results_data:
        report = get_forecast_report(dataset_id)
        if report:
            return redirect(url_for('forecasting.dashboard', dataset_id=dataset_id))
        flash('No forecasting results found. Please run forecasting first.', 'warning')
        return redirect(url_for('forecasting.setup', dataset_id=dataset_id))

    is_valid, err_msg = _validate_forecast_results(results_data, dataset_id)
    if not is_valid:
        flash(f'Validation failed: {err_msg}', 'danger')
        return redirect(url_for('forecasting.setup', dataset_id=dataset_id))

    report = get_forecast_report(dataset_id)
    workflow_state = get_workflow_state(dataset_id)
    step_urls = wf_get_step_urls(dataset_id, 5, workflow_state)

    return render_template('forecast_results.html', dataset=dataset,
                           results=results_data, report=report,
                           dataset_id=dataset_id,
                           current_step=workflow_state['current'],
                           workflow_state=workflow_state, step_urls=step_urls)


@forecasting_bp.route('/forecasting/dashboard/<int:dataset_id>')
@login_required
def dashboard(dataset_id):
    dataset = get_dataset(dataset_id, session['user_id'])
    if not dataset:
        flash('Dataset not found.', 'danger')
        return redirect(url_for('dataset.list_datasets'))
    resp = require_step_completion(dataset_id, 5)
    if resp:
        return resp

    report = get_forecast_report(dataset_id)
    if not report:
        flash('No forecasting results found.', 'warning')
        return redirect(url_for('forecasting.setup', dataset_id=dataset_id))

    results_data = load_forecast_results(dataset_id) or {}
    workflow_state = get_workflow_state(dataset_id)
    step_urls = wf_get_step_urls(dataset_id, 5, workflow_state)

    return render_template('forecast_dashboard.html', dataset=dataset,
                           report=report, results=results_data,
                           dataset_id=dataset_id,
                           current_step=workflow_state['current'],
                           workflow_state=workflow_state, step_urls=step_urls)


def _generate_download_rows(results_data):
    rows = []
    future_preds = results_data.get('future_predictions', [])
    for r in future_preds:
        rows.append({
            'Period': r.get('index', ''),
            'Forecast Date': r.get('date', ''),
            'Forecast Value': r.get('value', ''),
            'Lower CI (95%)': r.get('lower_confidence', ''),
            'Upper CI (95%)': r.get('upper_confidence', ''),
            'Prediction Interval': r.get('prediction_interval', ''),
            'Confidence %': r.get('confidence_percentage', ''),
            'Trend': r.get('trend', ''),
            'Status': r.get('status', ''),
        })

    actual_preds = results_data.get('actual_predictions', [])
    for r in actual_preds:
        rows.append({
            'Period': r.get('index', ''),
            'Forecast Date': r.get('date', ''),
            'Actual': r.get('actual', ''),
            'Predicted': r.get('predicted', ''),
            'Residual': r.get('residual', ''),
            'Absolute Error': r.get('absolute_error', ''),
            '% Error': r.get('percentage_error', ''),
            'Accuracy %': r.get('accuracy', ''),
            'Status': r.get('status', ''),
        })
    return rows


@forecasting_bp.route('/forecasting/download/<int:dataset_id>')
@login_required
def download_forecast(dataset_id):
    dataset = get_dataset(dataset_id, session['user_id'])
    if not dataset:
        flash('Dataset not found.', 'danger')
        return redirect(url_for('dataset.list_datasets'))
    resp = require_step_completion(dataset_id, 5)
    if resp:
        return resp

    results_data = load_forecast_results(dataset_id)
    if not results_data:
        flash('No forecast results found.', 'warning')
        return redirect(url_for('forecasting.dashboard', dataset_id=dataset_id))

    fmt = request.args.get('format', 'csv')
    base_name = f'forecast_{dataset.file_name.rsplit(".", 1)[0]}'
    rows = _generate_download_rows(results_data)

    if fmt == 'csv':
        output = io.StringIO()
        all_keys = list(dict.fromkeys(k for r in rows for k in r.keys())) if rows else []
        writer = csv.DictWriter(output, fieldnames=all_keys)
        writer.writeheader()
        writer.writerows(rows)
        mem = io.BytesIO(output.getvalue().encode('utf-8'))
        return send_file(mem, mimetype='text/csv', as_attachment=True,
                         download_name=f'{base_name}.csv')

    elif fmt == 'excel':
        df = pd.DataFrame(rows)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Forecast Results', index=False)
        output.seek(0)
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                         as_attachment=True, download_name=f'{base_name}.xlsx')

    elif fmt == 'pdf':
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

            output = io.BytesIO()
            doc = SimpleDocTemplate(output, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []

            ds_name = dataset.dataset_name or dataset.file_name
            elements.append(Paragraph(f'Forecast Results — {ds_name}', styles['Title']))
            elements.append(Paragraph(f'<b>Dataset ID:</b> {dataset.dataset_id}', styles['Normal']))
            elements.append(Spacer(1, 12))

            best = results_data.get('best_model', 'N/A')
            elements.append(Paragraph(f'<b>Best Model:</b> {best}', styles['Normal']))
            elements.append(Spacer(1, 12))

            if rows:
                headers = list(dict.fromkeys(k for r in rows for k in r.keys()))
                table_data = [headers]
                for r in rows:
                    table_data.append([str(r.get(h, '')) for h in headers])
                t = Table(table_data, repeatRows=1)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 7),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
                ]))
                elements.append(t)

            doc.build(elements)
            output.seek(0)
            return send_file(output, mimetype='application/pdf', as_attachment=True,
                             download_name=f'{base_name}.pdf')
        except ImportError:
            flash('PDF generation requires reportlab. Install with: pip install reportlab', 'warning')
            return redirect(url_for('forecasting.results', dataset_id=dataset_id))

    elif fmt == 'html':
        future_preds = results_data.get('future_predictions', [])
        actual_preds = results_data.get('actual_predictions', [])
        mm = results_data.get('model_metrics', {})
        fstats = results_data.get('forecast_statistics', {})
        ins = results_data.get('model_insights', {})

        html_rows_future = ''
        for r in future_preds:
            html_rows_future += f'<tr><td>{r.get("index","")}</td><td>{r.get("date","")}</td><td>{r.get("value","")}</td><td>{r.get("lower_confidence","")}</td><td>{r.get("upper_confidence","")}</td><td>{r.get("trend","")}</td></tr>\n'

        html_rows_actual = ''
        for r in actual_preds[:50]:
            html_rows_actual += f'<tr><td>{r.get("index","")}</td><td>{r.get("date","")}</td><td>{r.get("actual","")}</td><td>{r.get("predicted","")}</td><td>{r.get("residual","")}</td><td>{r.get("percentage_error","")}%</td><td>{r.get("status","")}</td></tr>\n'

        insights_html = ''
        if isinstance(ins, dict):
            for k, v in ins.items():
                if v:
                    label = k.replace('_', ' ').title()
                    insights_html += f'<p><strong>{label}:</strong> {v}</p>'
            if insights_html:
                insights_html = f'<div class="section"><h2>Intelligent Insights</h2>{insights_html}</div>'

        ds_name = dataset.dataset_name or dataset.file_name
        html_content = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Forecast Results — {ds_name}</title>
<style>
  body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; color: #333; }}
  h1 {{ color: #2563EB; border-bottom: 2px solid #2563EB; padding-bottom: 10px; }}
  h2 {{ color: #2563EB; margin-top: 30px; }}
  table {{ border-collapse: collapse; width: 100%; margin: 15px 0; font-size: 13px; }}
  th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
  th {{ background: #2563EB; color: white; }}
  tr:nth-child(even) {{ background: #f8fafc; }}
  .section {{ margin: 20px 0; padding: 15px; background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
  .footer {{ margin-top: 40px; text-align: center; color: #888; font-size: 12px; }}
  .stat-grid {{ display: flex; gap: 15px; flex-wrap: wrap; margin: 15px 0; }}
  .stat-item {{ background: #f8fafc; border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px 20px; text-align: center; flex: 1; min-width: 120px; }}
  .stat-value {{ font-size: 1.4rem; font-weight: 700; color: #111827; }}
  .stat-label {{ font-size: 0.75rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; }}
</style></head><body>
<h1>Forecast Results — {ds_name}</h1>
<p>Dataset ID: <strong>{dataset.dataset_id}</strong> | Best Model: <strong>{results_data.get("best_model", "N/A")}</strong> | Target: {results_data.get("target_column", "N/A")} | Horizon: {results_data.get("horizon", 0)} periods</p>

<div class="section">
<h2>Forecast Statistics</h2>
<div class="stat-grid">
  <div class="stat-item"><div class="stat-value">{fstats.get("minimum","N/A")}</div><div class="stat-label">Minimum</div></div>
  <div class="stat-item"><div class="stat-value">{fstats.get("maximum","N/A")}</div><div class="stat-label">Maximum</div></div>
  <div class="stat-item"><div class="stat-value">{fstats.get("average","N/A")}</div><div class="stat-label">Average</div></div>
  <div class="stat-item"><div class="stat-value">{fstats.get("median","N/A")}</div><div class="stat-label">Median</div></div>
  <div class="stat-item"><div class="stat-value">{fstats.get("std","N/A")}</div><div class="stat-label">Std Dev</div></div>
  <div class="stat-item"><div class="stat-value">{fstats.get("forecast_sum","N/A")}</div><div class="stat-label">Sum</div></div>
</div>
</div>

<div class="section">
<h2>Model Performance</h2>
<table>
<tr><th>Metric</th><th>Value</th></tr>
<tr><td>RMSE</td><td>{mm.get("rmse","N/A")}</td></tr>
<tr><td>MAE</td><td>{mm.get("mae","N/A")}</td></tr>
<tr><td>MAPE (%)</td><td>{mm.get("mape","N/A")}</td></tr>
<tr><td>R²</td><td>{mm.get("r2","N/A")}</td></tr>
<tr><td>Prediction Accuracy (%)</td><td>{mm.get("prediction_accuracy","N/A")}</td></tr>
<tr><td>Training Time (s)</td><td>{mm.get("training_time","N/A")}</td></tr>
</table>
</div>

<div class="section">
<h2>Future Forecast ({len(future_preds)} periods)</h2>
<table><tr><th>#</th><th>Date</th><th>Forecast Value</th><th>Lower CI</th><th>Upper CI</th><th>Trend</th></tr>
{html_rows_future}</table>
</div>

<div class="section">
<h2>Actual vs Predicted</h2>
<table><tr><th>#</th><th>Date</th><th>Actual</th><th>Predicted</th><th>Residual</th><th>% Error</th><th>Status</th></tr>
{html_rows_actual}</table>
</div>

{insights_html}

<div class="footer">Generated by ForecastIQ Forecasting Engine</div>
</body></html>'''

        mem = io.BytesIO(html_content.encode('utf-8'))
        return send_file(mem, mimetype='text/html', as_attachment=True,
                         download_name=f'{base_name}.html')

    else:
        flash(f'Unsupported format: {fmt}', 'warning')
        return redirect(url_for('forecasting.results', dataset_id=dataset_id))