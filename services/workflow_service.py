from flask import url_for, flash, redirect
from database import db
from models.dataset_model import Dataset
from models.validation_report_model import ValidationReport
from models.eda_report_model import EDAReport
from models.preprocessing_report_model import PreprocessingReport
from models.forecast_report_model import ForecastReport

STEPS = [
    {'number': 1, 'name': 'Upload', 'icon': 'fa-upload', 'route': 'dataset.upload'},
    {'number': 2, 'name': 'Validation', 'icon': 'fa-clipboard-check', 'route': 'dataset.validation_dashboard'},
    {'number': 3, 'name': 'EDA', 'icon': 'fa-chart-pie', 'route': 'eda.eda_dashboard'},
    {'number': 4, 'name': 'Preprocessing', 'icon': 'fa-filter', 'route': 'preprocessing.dashboard'},
    {'number': 5, 'name': 'Forecasting', 'icon': 'fa-chart-line', 'route': 'forecasting.dashboard'},
    {'number': 6, 'name': 'Reports', 'icon': 'fa-file-alt', 'route': 'reports.view_report'},
]


def _report_exists_for_step(dataset_id, step_number):
    if step_number == 2:
        report = ValidationReport.query.filter_by(dataset_id=dataset_id).order_by(
            ValidationReport.created_at.desc()).first()
        return report is not None and report.validation_status == 'completed'
    if step_number == 3:
        return EDAReport.query.filter_by(dataset_id=dataset_id).first() is not None
    if step_number == 4:
        return PreprocessingReport.query.filter_by(dataset_id=dataset_id).order_by(
            PreprocessingReport.created_at.desc()).first() is not None
    if step_number == 5:
        return ForecastReport.query.filter_by(dataset_id=dataset_id).order_by(
            ForecastReport.created_at.desc()).first() is not None
    if step_number == 6:
        return True
    return False


def _get_workflow_step(dataset_id):
    dataset = Dataset.query.get(dataset_id)
    if not dataset:
        return 1
    return dataset.workflow_step or 1


def _set_workflow_step(dataset_id, step, force=False):
    dataset = Dataset.query.get(dataset_id)
    if dataset and (force or dataset.workflow_step < step):
        dataset.workflow_step = step
        db.session.commit()


def get_workflow_state(dataset_id):
    step = _get_workflow_step(dataset_id)
    completed = list(range(1, step + 1))
    locked = list(range(step + 2, 7))
    current = step + 1 if step < 6 else 6
    return {'steps': STEPS, 'completed': completed, 'current': current, 'locked': locked}

def complete_step(dataset_id):
    step = _get_workflow_step(dataset_id)
    if step < 6:
        _set_workflow_step(dataset_id, step + 1)


def require_step_completion(dataset_id, step_number):
    if step_number <= 1:
        return None
    state = get_workflow_state(dataset_id)
    prev_step = step_number - 1
    if prev_step not in state['completed']:
        if _report_exists_for_step(dataset_id, prev_step):
            _set_workflow_step(dataset_id, prev_step)
            return None
        flash('Please complete the previous step before accessing this section.', 'warning')
        prev_url = _build_step_url_by_number(prev_step, dataset_id, state['completed'])
        if prev_url:
            return redirect(prev_url)
        return redirect(url_for('dataset.list_datasets'))
    return None


def get_step_urls(dataset_id, page_step, workflow_state):
    completed = workflow_state['completed']
    prev = None
    if page_step > 1:
        prev = _build_step_url_by_number(page_step - 1, dataset_id, completed)
    next_url = None
    next_step = page_step + 1
    if page_step in completed and next_step <= 6:
        next_url = _build_step_url_by_number(next_step, dataset_id, completed)


    return {'prev': prev, 'next': next_url}


def _build_step_url_by_number(step_number, dataset_id, completed=None):
    for step in STEPS:
        if step['number'] == step_number:
            return _build_step_url(step, dataset_id, completed)
    return None


def _build_step_url(step, dataset_id, completed=None):
    if completed is None:
        completed = []
    route = step.get('route')
    if not route:
        return None
    if step['number'] == 1:
        return url_for('dataset.upload')
    if step['number'] == 2:
        return url_for('dataset.validation_dashboard', dataset_id=dataset_id)
    if step['number'] == 3:
        if 3 in completed:
            return url_for('eda.eda_dashboard', dataset_id=dataset_id)
        return url_for('eda.mode_selection', dataset_id=dataset_id)
    if step['number'] == 4:
        if 4 in completed:
            return url_for('preprocessing.dashboard', dataset_id=dataset_id)
        return url_for('preprocessing.mode_selection', dataset_id=dataset_id)
    if step['number'] == 5:
        if 5 in completed:
            return url_for('forecasting.dashboard', dataset_id=dataset_id)
        return url_for('forecasting.setup', dataset_id=dataset_id)
    if step['number'] == 6:
        return url_for('reports.view_report', dataset_id=dataset_id)
    return url_for(route, dataset_id=dataset_id)
