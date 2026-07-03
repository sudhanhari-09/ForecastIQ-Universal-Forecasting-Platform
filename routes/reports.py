import os
from flask import (Blueprint, current_app, render_template, request,
                   redirect, url_for, flash, session, send_file, jsonify)
from routes.auth import login_required
from services.dataset_service import get_dataset
from services.report_service import (
    get_report_context, generate_report_csv,
    generate_report_excel, generate_report_pdf,
    save_analysis_history
)
from services.activity_service import log_activity
from services.model_download_service import validate_model_package, create_model_zip
from services.workflow_service import get_workflow_state, get_step_urls as wf_get_step_urls, require_step_completion, complete_step
from datetime import datetime

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/reports/<int:dataset_id>')
@login_required
def view_report(dataset_id):
    dataset = get_dataset(dataset_id, session['user_id'])
    if not dataset:
        flash('Dataset not found.', 'danger')
        return redirect(url_for('dataset.list_datasets'))
    resp = require_step_completion(dataset_id, 6)
    if resp:
        return resp

    context, error = get_report_context(dataset_id)
    if error:
        flash(error, 'danger')
        return redirect(url_for('dataset.detail', dataset_id=dataset_id))
    if context is None:
        flash('No report data available. Complete the workflow first.', 'warning')
        return redirect(url_for('dataset.detail', dataset_id=dataset_id))

    workflow_state = get_workflow_state(dataset_id)
    step_urls = wf_get_step_urls(dataset_id, 6, workflow_state)

    prev_url = step_urls.get('prev')
    next_url = step_urls.get('next')

    log_activity(session['user_id'], 'viewed_report', 'report', dataset_id)
    save_analysis_history(dataset_id, session['user_id'])
    complete_step(dataset_id)

    return render_template(
        'report_view.html',
        dataset=dataset,
        dataset_id=dataset_id,
        report=context,
        workflow_state=workflow_state,
        step_urls=step_urls,
        prev_url=prev_url,
        next_url=next_url,
        current_step=6,
        now=datetime.utcnow(),
        enumerate=enumerate,
    )


@reports_bp.route('/workflow/completed/<int:dataset_id>')
@login_required
def workflow_completed(dataset_id):
    dataset = get_dataset(dataset_id, session['user_id'])
    if not dataset:
        flash('Dataset not found.', 'danger')
        return redirect(url_for('dataset.list_datasets'))
    resp = require_step_completion(dataset_id, 6)
    if resp:
        return resp

    context, error = get_report_context(dataset_id)
    if error or not context:
        flash('Complete the workflow first.', 'warning')
        return redirect(url_for('dataset.detail', dataset_id=dataset_id))

    workflow_state = get_workflow_state(dataset_id)
    step_urls = wf_get_step_urls(dataset_id, 6, workflow_state)

    prev_url = step_urls.get('prev')
    next_url = step_urls.get('next')

    log_activity(session['user_id'], 'workflow_completed', 'workflow', dataset_id)
    save_analysis_history(dataset_id, session['user_id'])

    return render_template(
        'workflow_completed.html',
        dataset=dataset,
        dataset_id=dataset_id,
        report=context,
        workflow_state=workflow_state,
        step_urls=step_urls,
        prev_url=prev_url,
        next_url=next_url,
        current_step=6,
        now=datetime.utcnow(),
    )


@reports_bp.route('/reports/download/<int:dataset_id>/<file_format>')
@login_required
def download_report(dataset_id, file_format):
    dataset = get_dataset(dataset_id, session['user_id'])
    if not dataset:
        flash('Dataset not found.', 'danger')
        return redirect(url_for('dataset.list_datasets'))
    resp = require_step_completion(dataset_id, 6)
    if resp:
        return resp

    generators = {
        'csv': generate_report_csv,
        'xlsx': generate_report_excel,
        'pdf': generate_report_pdf,
    }

    gen = generators.get(file_format)
    if not gen:
        flash(f'Unsupported format: {file_format}', 'danger')
        return redirect(url_for('reports.view_report', dataset_id=dataset_id))

    path, error = gen(dataset_id)
    if error:
        flash(error, 'danger')
        return redirect(url_for('reports.view_report', dataset_id=dataset_id))

    mime_types = {
        'csv': 'text/csv',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'pdf': 'application/pdf',
    }
    return send_file(
        path,
        mimetype=mime_types.get(file_format, 'application/octet-stream'),
        as_attachment=True,
        download_name=f'forecast_report_{dataset_id}.{file_format}'
    )


@reports_bp.route('/reports/download-model/<int:dataset_id>')
@login_required
def download_trained_model(dataset_id):
    dataset = get_dataset(dataset_id, session['user_id'])
    if not dataset:
        flash('Dataset not found.', 'danger')
        return redirect(url_for('dataset.list_datasets'))
    resp = require_step_completion(dataset_id, 6)
    if resp:
        return resp

    valid, err = validate_model_package(dataset_id)
    if not valid:
        flash(f'Model download unavailable: {err}', 'danger')
        return redirect(url_for('reports.view_report', dataset_id=dataset_id))

    buf, err = create_model_zip(dataset_id, dataset_name=dataset.file_name)
    if err or buf is None:
        flash(f'Failed to create model package: {err}', 'danger')
        return redirect(url_for('reports.view_report', dataset_id=dataset_id))

    import json
    model_dir = os.path.join(
        current_app.config.get('PROCESSED_FOLDER', 'data/processed'),
        '..', 'forecasts', str(dataset_id), 'trained_model'
    )
    model_dir = os.path.normpath(model_dir)
    meta_path = os.path.join(model_dir, 'metadata.json')
    zip_name = 'TrainedModel.zip'
    if os.path.exists(meta_path):
        try:
            with open(meta_path, 'r') as f:
                meta = json.load(f)
            model_name = meta.get('forecast_model', 'Model')
            zip_name = f'{model_name}_Model.zip'
        except Exception:
            pass

    return send_file(
        buf,
        mimetype='application/zip',
        as_attachment=True,
        download_name=zip_name
    )
