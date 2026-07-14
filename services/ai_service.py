import json
import logging
from itsdangerous import URLSafeSerializer
from flask import current_app, session
from database import db
from models.ai_settings_model import AISettings
from models.dataset_model import Dataset
from models.validation_report_model import ValidationReport
from models.eda_report_model import EDAReport
from models.preprocessing_report_model import PreprocessingReport
from models.forecast_report_model import ForecastReport
from models.comparison_report_model import ComparisonReport
from services.providers.openai_provider import query_openai
from services.providers.gemini_provider import query_gemini
from services.providers.openrouter_provider import query_openrouter
from services.forecasting_service import load_forecast_results
from services.comparison_service import load_comparison_results
from services.report_service import load_report_results

logger = logging.getLogger(__name__)

PROVIDER_MAP = {
    'openai': query_openai,
    'gemini': query_gemini,
    'openrouter': query_openrouter,
}

DEFAULT_SYSTEM_PROMPT = """You are ForecastIQ AI Copilot, an intelligent forecasting assistant integrated into the ForecastIQ platform. Your role is to help users understand their data, forecasts, and model results.

Key guidelines:
1. Only answer questions related to the user's dataset, workflow, forecasts, and platform features.
2. Use the provided context information to give specific, accurate answers.
3. If you don't have enough context, ask the user to complete the relevant workflow step first.
4. Explain technical concepts (RMSE, MAE, MAPE, R2, etc.) in clear, simple terms.
5. Be concise but thorough in your explanations.
6. Never make up data - only use what's provided in the context.
7. When suggesting improvements, be practical and actionable.
8. Reference specific numbers and metrics from the context when available.
9. Format responses with clear sections when appropriate.
10. Stay professional and helpful."""


def get_serializer():
    return URLSafeSerializer(current_app.config['SECRET_KEY'])


def encrypt_key(api_key):
    s = get_serializer()
    return s.dumps(api_key)


def decrypt_key(encrypted):
    try:
        s = get_serializer()
        return s.loads(encrypted)
    except Exception as e:
        logger.error("Failed to decrypt API key: %s", e)
        return ''


def get_user_settings(user_id):
    settings = AISettings.query.filter_by(user_id=user_id).first()
    return settings


def save_user_settings(user_id, provider, api_key, model, temperature, max_tokens):
    settings = AISettings.query.filter_by(user_id=user_id).first()
    if not settings:
        settings = AISettings(user_id=user_id)
        db.session.add(settings)

    settings.provider = provider
    if api_key:
        settings.api_key_encrypted = encrypt_key(api_key)
    settings.model = model
    settings.temperature = temperature
    settings.max_tokens = max_tokens
    db.session.commit()
    return settings


def mask_api_key(api_key):
    if not api_key or len(api_key) < 8:
        return '****'
    return api_key[:4] + '****' + api_key[-4:]


def get_dataset_context(dataset_id):
    if not dataset_id:
        return {}
    dataset = Dataset.query.get(dataset_id)
    if not dataset:
        return {}

    ctx = {
        'dataset_name': dataset.dataset_name,
        'dataset_id': dataset.id,
        'dataset_id_display': dataset.dataset_id,
        'file_name': dataset.file_name,
        'rows': dataset.rows_count,
        'columns': dataset.columns_count,
        'workflow_step': dataset.workflow_step,
        'upload_date': str(dataset.upload_date) if dataset.upload_date else None,
    }

    validation = ValidationReport.query.filter_by(dataset_id=dataset_id).order_by(
        ValidationReport.created_at.desc()
    ).first()
    if validation and validation.validation_status == 'completed':
        try:
            ctx['validation'] = {
                'status': validation.validation_status,
                'total_rows': validation.total_rows,
                'total_columns': validation.total_columns,
                'missing_values': json.loads(validation.missing_values) if validation.missing_values else [],
                'duplicate_rows': validation.duplicate_rows,
                'empty_columns': json.loads(validation.empty_columns) if validation.empty_columns else [],
                'duplicate_columns': json.loads(validation.duplicate_columns) if validation.duplicate_columns else [],
                'date_columns': json.loads(validation.date_columns) if validation.date_columns else [],
                'numeric_columns': json.loads(validation.numeric_columns) if validation.numeric_columns else [],
                'categorical_columns': json.loads(validation.categorical_columns) if validation.categorical_columns else [],
            }
        except (json.JSONDecodeError, TypeError) as e:
            logger.warning("Failed to parse validation report JSON: %s", e)

    eda = EDAReport.query.filter_by(dataset_id=dataset_id).order_by(
        EDAReport.generated_at.desc()
    ).first()
    if eda:
        ctx['eda'] = {
            'mode': eda.eda_mode,
            'total_charts': eda.total_charts,
        }

    prep = PreprocessingReport.query.filter_by(dataset_id=dataset_id).order_by(
        PreprocessingReport.created_at.desc()
    ).first()
    if prep:
        try:
            steps = json.loads(prep.steps_applied) if prep.steps_applied else {}
            ctx['preprocessing'] = {
                'mode': prep.mode,
                'original_shape': prep.original_shape,
                'processed_shape': prep.processed_shape,
                'steps_applied': steps,
            }
        except (json.JSONDecodeError, TypeError) as e:
            logger.warning("Failed to parse preprocessing steps: %s", e)

    forecast_report = ForecastReport.query.filter_by(dataset_id=dataset_id).order_by(
        ForecastReport.created_at.desc()
    ).first()
    if forecast_report:
        ctx['forecast'] = {
            'model_name': forecast_report.model_name,
            'forecast_horizon': forecast_report.forecast_horizon,
            'target_column': forecast_report.target_column,
            'date_column': forecast_report.date_column,
            'mae': float(forecast_report.mae) if forecast_report.mae is not None else None,
            'rmse': float(forecast_report.rmse) if forecast_report.rmse is not None else None,
            'mape': float(forecast_report.mape) if forecast_report.mape is not None else None,
            'r2': float(forecast_report.r2_score) if forecast_report.r2_score is not None else None,
        }

        try:
            forecast_results = load_forecast_results(dataset_id)
        except Exception:
            logger.warning("Failed to load forecast results for dataset %s", dataset_id)
            forecast_results = None
        if forecast_results and 'models' in forecast_results:
            models_data = {}
            for mname, mdata in forecast_results['models'].items():
                if mdata.get('status') == 'success' and mdata.get('metrics'):
                    models_data[mname] = {
                        'status': 'success',
                        'metrics': mdata['metrics'],
                        'training_time': mdata.get('params', {}).get('training_time'),
                    }
                else:
                    models_data[mname] = {
                        'status': 'failed',
                        'error': mdata.get('error', 'Unknown error'),
                    }
            ctx['forecast']['all_models'] = models_data

    comparison = ComparisonReport.query.filter_by(dataset_id=dataset_id).order_by(
        ComparisonReport.created_at.desc()
    ).first()
    if comparison:
        ctx['comparison'] = {
            'best_model': comparison.best_model,
            'ranking': comparison.ranking,
        }
        try:
            comparison_results = load_comparison_results(dataset_id)
        except Exception:
            logger.warning("Failed to load comparison results for dataset %s", dataset_id)
            comparison_results = None
        if comparison_results:
            ctx['comparison']['details'] = comparison_results

    try:
        report_results = load_report_results(dataset_id)
    except Exception:
        logger.warning("Failed to load report results for dataset %s", dataset_id)
        report_results = None
    if report_results:
        ctx['report'] = {
            'best_model': report_results.get('best_model'),
            'best_rmse': report_results.get('best_rmse'),
            'best_mae': report_results.get('best_mae'),
            'best_mape': report_results.get('best_mape'),
            'best_r2': report_results.get('best_r2'),
            'smart_insights': report_results.get('smart_insights', []),
        }

    return ctx


def build_system_prompt(context, page_context=None):
    page_context = page_context or {}
    parts = [DEFAULT_SYSTEM_PROMPT]

    parts.append("\n\n## CURRENT WORKFLOW CONTEXT")

    if page_context:
        page = page_context.get('page', '')
        dataset_id = page_context.get('dataset_id')
        parts.append(f"- Active Page: {page}")
        if dataset_id:
            parts.append(f"- Dataset ID: {dataset_id}")

    ds = context.get('dataset_name')
    if ds:
        parts.append(f"\n### Dataset Information")
        parts.append(f"- Name: {ds}")
        parts.append(f"- Rows: {context.get('rows', 'N/A')}")
        parts.append(f"- Columns: {context.get('columns', 'N/A')}")

    val = context.get('validation')
    if val:
        parts.append(f"\n### Validation Summary")
        parts.append(f"- Status: {val.get('status', 'N/A')}")
        parts.append(f"- Total Rows: {val.get('total_rows', 'N/A')}")
        parts.append(f"- Total Columns: {val.get('total_columns', 'N/A')}")
        parts.append(f"- Duplicate Rows: {val.get('duplicate_rows', 0)}")
        mv = val.get('missing_values', [])
        if mv:
            parts.append(f"- Missing Values: {len(mv)} columns affected ({sum(m.get('count', 0) for m in mv)} total)")
        parts.append(f"- Date Columns: {', '.join(val.get('date_columns', []))}")
        parts.append(f"- Numeric Columns: {', '.join(val.get('numeric_columns', []))}")
        parts.append(f"- Categorical Columns: {', '.join(val.get('categorical_columns', []))}")

    eda = context.get('eda')
    if eda:
        parts.append(f"\n### EDA Summary")
        parts.append(f"- Mode: {eda.get('mode', 'N/A')}")
        parts.append(f"- Total Charts Generated: {eda.get('total_charts', 0)}")

    prep = context.get('preprocessing')
    if prep:
        parts.append(f"\n### Preprocessing Summary")
        parts.append(f"- Mode: {prep.get('mode', 'N/A')}")
        parts.append(f"- Original Shape: {prep.get('original_shape', 'N/A')}")
        parts.append(f"- Processed Shape: {prep.get('processed_shape', 'N/A')}")
        steps = prep.get('steps_applied', {})
        if steps:
            for step_name, step_data in steps.items():
                if isinstance(step_data, dict):
                    method = step_data.get('method', 'none')
                    if method != 'none':
                        parts.append(f"- {step_name.replace('_', ' ').title()}: {method}")

    fc = context.get('forecast')
    if fc:
        parts.append(f"\n### Forecast Results")
        parts.append(f"- Model: {fc.get('model_name', 'N/A')}")
        parts.append(f"- Target: {fc.get('target_column', 'N/A')}")
        parts.append(f"- Horizon: {fc.get('forecast_horizon', 'N/A')} periods")
        parts.append(f"- RMSE: {fc.get('rmse', 'N/A')}")
        parts.append(f"- MAE: {fc.get('mae', 'N/A')}")
        parts.append(f"- MAPE: {fc.get('mape', 'N/A')}%")
        parts.append(f"- R²: {fc.get('r2', 'N/A')}")

        all_models = fc.get('all_models', {})
        if all_models:
            parts.append(f"\n### All Trained Models")
            for mname, mdata in all_models.items():
                if mdata.get('status') == 'success':
                    m = mdata.get('metrics', {})
                    parts.append(f"- {mname}: RMSE={m.get('rmse', 'N/A')}, MAE={m.get('mae', 'N/A')}, R²={m.get('r2', 'N/A')}")
                else:
                    parts.append(f"- {mname}: Failed ({mdata.get('error', 'Unknown error')})")

    comp = context.get('comparison')
    if comp:
        parts.append(f"\n### Comparison Results")
        parts.append(f"- Best Model: {comp.get('best_model', 'N/A')}")
        if comp.get('ranking'):
            parts.append(f"- Ranking: {comp.get('ranking')}")

    rpt = context.get('report')
    if rpt:
        parts.append(f"\n### Report Summary")
        parts.append(f"- Best Model: {rpt.get('best_model', 'N/A')}")
        parts.append(f"- Best RMSE: {rpt.get('best_rmse', 'N/A')}")
        parts.append(f"- Best MAE: {rpt.get('best_mae', 'N/A')}")
        parts.append(f"- Best MAPE: {rpt.get('best_mape', 'N/A')}%")
        parts.append(f"- Best R²: {rpt.get('best_r2', 'N/A')}")
        insights = rpt.get('smart_insights', [])
        if insights:
            parts.append(f"\n### Generated Insights")
            for insight in insights:
                parts.append(f"- {insight}")

    parts.append("\n\nBased on the above context, answer the user's question accurately and helpfully. If the context lacks information to answer, suggest the user complete the relevant workflow step first.")

    return '\n'.join(parts)


def chat_with_ai(user_id, dataset_id, message, conversation_history, page_context=None):
    settings = get_user_settings(user_id)
    if not settings or not settings.api_key_encrypted:
        return None, "AI Copilot is not configured. Please go to Settings → AI Copilot to set up your AI provider."

    api_key = decrypt_key(settings.api_key_encrypted)
    if not api_key:
        return None, "AI Copilot configuration is invalid. Please reconfigure in Settings → AI Copilot."

    provider = settings.provider or 'openai'
    model = settings.model or 'gpt-4o-mini'
    temperature = settings.temperature or 0.7
    max_tokens = settings.max_tokens or 2048

    query_fn = PROVIDER_MAP.get(provider)
    if not query_fn:
        return None, f"Unsupported AI provider: {provider}"

    context = get_dataset_context(dataset_id)
    system_prompt = build_system_prompt(context, page_context)

    messages = [{"role": "system", "content": system_prompt}]
    for msg in conversation_history:
        role = msg.get('role', 'user')
        content = msg.get('content', '')
        if role in ('user', 'assistant'):
            messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": message})

    try:
        response = query_fn(api_key, model, messages, temperature, max_tokens)
        return context, response
    except Exception as e:
        logger.error("AI chat error: %s", str(e))
        return context, f"Error communicating with {provider}: {str(e)}"
