import os
from datetime import datetime, timedelta
import pandas as pd
from flask import current_app
from database import db
from models.dataset_model import Dataset
from models.user_model import User
from models.forecast_report_model import ForecastReport
from models.validation_report_model import ValidationReport
from sqlalchemy import or_, and_, exists
from utils.file_utils import allowed_file, save_uploaded_file


def get_upload_folder():
    return current_app.config.get('UPLOAD_FOLDER', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'uploads'))


def generate_dataset_id():
    today = datetime.utcnow().strftime('%Y%m%d')
    prefix = f'DS-{today}-'
    last = Dataset.query.filter(
        Dataset.dataset_id.like(f'{prefix}%')
    ).order_by(Dataset.dataset_id.desc()).first()
    if last:
        last_seq = int(last.dataset_id.split('-')[-1])
        new_seq = last_seq + 1
    else:
        new_seq = 1
    return f'{prefix}{new_seq:06d}'


def read_dataframe(file_path, extension, nrows=None):
    try:
        if extension == 'csv':
            return pd.read_csv(file_path, nrows=nrows)
        elif extension in ('xls', 'xlsx'):
            return pd.read_excel(file_path, nrows=nrows)
        return None
    except Exception:
        return None


def upload_dataset(file, user_id, dataset_name=None):
    if not file or not allowed_file(file.filename):
        return None, 'Invalid file type. Allowed: CSV, XLS, XLSX.'

    upload_folder = get_upload_folder()
    os.makedirs(upload_folder, exist_ok=True)

    if not dataset_name or not dataset_name.strip():
        dataset_name = os.path.splitext(file.filename)[0]
    dataset_name = dataset_name.strip()

    file_info = save_uploaded_file(file, upload_folder)
    extension = file_info['extension']

    df = read_dataframe(file_info['file_path'], extension)
    if df is None:
        os.remove(file_info['file_path'])
        return None, 'Unable to read file. It may be corrupted.'

    if df.empty:
        os.remove(file_info['file_path'])
        return None, 'Uploaded file is empty.'

    dataset_id = generate_dataset_id()

    dataset = Dataset(
        user_id=user_id,
        dataset_name=dataset_name,
        dataset_id=dataset_id,
        file_name=file_info['original_name'],
        file_path=file_info['file_path'],
        file_size=file_info['file_size'],
        rows_count=len(df),
        columns_count=len(df.columns),
        workflow_step=1
    )
    db.session.add(dataset)
    db.session.commit()
    return dataset, None


def get_user_datasets(user_id, page=1, per_page=10, search='', sort='newest',
                      date_filter='all', date_from='', date_to='',
                      model_filter='', status_filter=''):
    query = Dataset.query.filter_by(user_id=user_id)

    if search:
        query = query.filter(
            or_(
                Dataset.dataset_name.ilike(f'%{search}%'),
                Dataset.dataset_id.ilike(f'%{search}%')
            )
        )

    if date_filter == 'today':
        query = query.filter(Dataset.upload_date >= datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0))
    elif date_filter == '7days':
        query = query.filter(Dataset.upload_date >= datetime.utcnow() - timedelta(days=7))
    elif date_filter == '30days':
        query = query.filter(Dataset.upload_date >= datetime.utcnow() - timedelta(days=30))
    elif date_filter == 'custom':
        if date_from:
            query = query.filter(Dataset.upload_date >= datetime.strptime(date_from, '%Y-%m-%d'))
        if date_to:
            query = query.filter(Dataset.upload_date <= datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1))

    if status_filter == 'completed':
        subq = exists().where(
            and_(ValidationReport.dataset_id == Dataset.id, ValidationReport.validation_status == 'completed')
        )
        query = query.filter(subq)
    elif status_filter == 'failed':
        subq = exists().where(
            and_(ValidationReport.dataset_id == Dataset.id, ValidationReport.validation_status == 'failed')
        )
        query = query.filter(subq)
    elif status_filter == 'pending':
        subq = exists().where(
            and_(ValidationReport.dataset_id == Dataset.id, ValidationReport.validation_status.in_(['completed', 'failed']))
        )
        query = query.filter(~subq)

    if model_filter:
        subq = exists().where(
            and_(ForecastReport.dataset_id == Dataset.id, ForecastReport.model_name == model_filter)
        )
        query = query.filter(subq)

    if sort == 'oldest':
        query = query.order_by(Dataset.upload_date.asc())
    elif sort == 'name_az':
        query = query.order_by(Dataset.dataset_name.asc())
    elif sort == 'name_za':
        query = query.order_by(Dataset.dataset_name.desc())
    else:
        query = query.order_by(Dataset.upload_date.desc())

    total = query.count()
    datasets = query.offset((page - 1) * per_page).limit(per_page).all()
    return datasets, total


def get_available_models(user_id):
    subq = db.session.query(ForecastReport.dataset_id).filter(
        Dataset.user_id == user_id,
        Dataset.id == ForecastReport.dataset_id
    ).exists()
    results = db.session.query(ForecastReport.model_name).filter(subq).distinct().all()
    return sorted([r[0] for r in results])


def get_dataset(dataset_id, user_id):
    return Dataset.query.filter_by(id=dataset_id, user_id=user_id).first()


def delete_dataset(dataset):
    file_path = dataset.file_path
    db.session.delete(dataset)
    db.session.commit()
    if os.path.exists(file_path):
        os.remove(file_path)
    return True


def get_preview_data(file_path, extension, rows=20):
    df = read_dataframe(file_path, extension, nrows=rows)

    if df is None:
        return None, None, None

    columns = list(df.columns)
    dtypes = {str(col): str(df[col].dtype) for col in df.columns}

    preview_df = df.copy()

    import re

    for col in preview_df.columns:
        if preview_df[col].dtype == object:
            try:
                converted = pd.to_datetime(preview_df[col], errors="raise")
                preview_df[col] = converted.dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                pass

    for col in preview_df.columns:
        try:
            # Handle timezone-aware datetime columns
            if "datetime" in str(preview_df[col].dtype).lower():
                preview_df[col] = (
                    preview_df[col]
                    .dt.tz_localize(None)
                    .dt.strftime("%Y-%m-%d %H:%M")
                )
        except Exception:
            pass

    data = preview_df.fillna("").values.tolist()

    return columns, data, dtypes

def get_column_info(file_path, extension):
    df = read_dataframe(file_path, extension)
    if df is None:
        return None, None
    return len(df), len(df.columns)


def get_column_detail_stats(file_path, extension):
    df = read_dataframe(file_path, extension, nrows=10000)
    if df is None:
        return {}
    stats = {}
    for col in df.columns:
        col_name = str(col)
        unique_count = int(df[col].nunique())
        non_null = df[col].dropna()
        example_val = str(non_null.iloc[0]) if len(non_null) > 0 else ''
        stats[col_name] = {
            'unique_count': unique_count,
            'example_value': example_val
        }
    return stats
