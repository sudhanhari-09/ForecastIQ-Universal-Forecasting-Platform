import json
import logging
import traceback
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.utils
from scipy import stats as scipy_stats


def sanitize_filename(name):
    invalid_chars = '/\\:*?"<>|'
    result = str(name)
    for ch in invalid_chars:
        result = result.replace(ch, '_')
    result = result.replace(' ', '_')
    return result


def _log_error(chart_name, column, error):
    traceback.print_exc()
    logging.error("Chart error - %s | Column: %s | %s", chart_name, column, error)


def _prepare_numeric(series, column):
    if series is None or len(series) == 0:
        _log_error('prepare_numeric', column, 'Empty series')
        return None
    cleaned = pd.to_numeric(series, errors='coerce')
    cleaned = cleaned.dropna()
    if len(cleaned) == 0:
        _log_error('prepare_numeric', column, 'No valid numeric values after conversion')
        return None
    cleaned = cleaned.replace([np.inf, -np.inf], np.nan).dropna()
    if len(cleaned) == 0:
        _log_error('prepare_numeric', column, 'No finite values after removing infinity')
        return None
    if cleaned.nunique() <= 1:
        _log_error('prepare_numeric', column, f'Constant column (single unique value: {cleaned.iloc[0]})')
        return None
    if len(cleaned) < 2:
        _log_error('prepare_numeric', column, f'Only {len(cleaned)} non-null value(s), need at least 2')
        return None
    return cleaned.astype(float)


def _validate_output(fig, chart_name, column):
    if fig is None:
        _log_error('validate_output', column, f'{chart_name}: Figure is None')
        return None
    try:
        data = fig.get('data') if isinstance(fig, dict) else fig.data
        if data is None or len(data) == 0:
            _log_error('validate_output', column, f'{chart_name}: No traces in figure')
            return None
        return fig
    except Exception as e:
        _log_error('validate_output', column, f'{chart_name}: Validation exception: {e}')
        return None


def _plotly_to_json(fig):
    return json.loads(json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder))


def histogram(df, column):
    data = _prepare_numeric(df[column], column)
    if data is None:
        return None
    fig = go.Figure(data=[go.Histogram(x=data, nbinsx=30, marker_color='#0d6efd')])
    fig.update_layout(title=f'Histogram — {column}', xaxis_title=column, yaxis_title='Frequency',
                      template='plotly_white', height=400, margin=dict(l=50, r=20, t=50, b=50))
    fig = _validate_output(fig, 'histogram', column)
    if fig is None:
        return None
    return _plotly_to_json(fig)


def density_plot(df, column):
    data = _prepare_numeric(df[column], column)
    if data is None or len(data) < 3:
        _log_error('density_plot', column, f'Need at least 3 points, got {len(data) if data is not None else 0}')
        return None
    try:
        kde = scipy_stats.gaussian_kde(data)
        x_range = np.linspace(data.min(), data.max(), 200)
        y_kde = kde(x_range)
        fig = go.Figure(data=[go.Scatter(
            x=x_range, y=y_kde, mode='lines',
            fill='tozeroy', line=dict(color='#0d6efd', width=2),
            name='Density'
        )])
        fig.update_layout(title=f'Density Plot — {column}',
                          xaxis_title=column, yaxis_title='Density',
                          template='plotly_white', height=400,
                          margin=dict(l=50, r=20, t=50, b=50))
        fig = _validate_output(fig, 'density_plot', column)
        if fig is None:
            return None
        return _plotly_to_json(fig)
    except Exception as e:
        _log_error('density_plot', column, e)
        return None


def boxplot(df, column):
    data = _prepare_numeric(df[column], column)
    if data is None:
        return None
    fig = go.Figure(data=[go.Box(y=data, name=column, marker_color='#0d6efd')])
    fig.update_layout(title=f'Box Plot — {column}', template='plotly_white', height=400,
                      margin=dict(l=50, r=20, t=50, b=50))
    fig = _validate_output(fig, 'boxplot', column)
    if fig is None:
        return None
    return _plotly_to_json(fig)


def correlation_heatmap(df):
    numeric_df = df.select_dtypes(include=[np.number]).copy()
    for col in numeric_df.columns:
        numeric_df[col] = pd.to_numeric(numeric_df[col], errors='coerce')
    numeric_df = numeric_df.dropna(axis=1, how='all').dropna(axis=0, how='all').reset_index(drop=True)
    if numeric_df.shape[1] < 2:
        _log_error('correlation_heatmap', '', 'Need at least 2 numeric columns with data')
        return None
    corr = numeric_df.corr().round(4)
    cols = corr.columns.tolist()
    z = corr.values
    fig = go.Figure(data=go.Heatmap(z=z, x=cols, y=cols, colorscale='RdBu_r', zmin=-1, zmax=1,
                                     text=np.round(z, 2), texttemplate='%{text}', textfont=dict(size=9)))
    fig.update_layout(title='Correlation Heatmap', template='plotly_white', height=500, width=600,
                      margin=dict(l=80, r=20, t=50, b=80))
    fig = _validate_output(fig, 'correlation_heatmap', 'all')
    if fig is None:
        return None
    return _plotly_to_json(fig)


def missing_values_chart(missing_data):
    if not missing_data:
        _log_error('missing_values_chart', '', 'No missing data provided')
        return None
    cols = [m['column'] for m in missing_data]
    vals = []
    for v in missing_data:
        try:
            vals.append(float(v['count']))
        except (ValueError, TypeError):
            vals.append(0)
    if len(cols) == 0:
        _log_error('missing_values_chart', '', 'Empty columns list')
        return None
    fig = go.Figure(data=[go.Bar(x=cols, y=vals, marker_color='#dc3545', text=vals, textposition='outside')])
    fig.update_layout(title='Missing Values by Column', xaxis_title='Column', yaxis_title='Missing Count',
                      template='plotly_white', height=400, margin=dict(l=50, r=20, t=50, b=80))
    fig = _validate_output(fig, 'missing_values_chart', 'all')
    if fig is None:
        return None
    return _plotly_to_json(fig)


def missing_heatmap(df):
    missing_binary = df.isnull().astype(int)
    total_missing = int(missing_binary.sum().sum())
    if total_missing == 0:
        _log_error('missing_heatmap', '', 'No missing values to plot')
        return None
    max_cols = 50
    cols = missing_binary.columns.tolist()
    if len(cols) > max_cols:
        cols = cols[:max_cols]
    plot_data = missing_binary[cols]
    max_rows = 2000
    if len(plot_data) > max_rows:
        indices = np.linspace(0, len(plot_data) - 1, max_rows, dtype=int)
        plot_data = plot_data.iloc[indices]
    fig = go.Figure(data=go.Heatmap(
        z=plot_data.T.values,
        x=list(range(len(plot_data))),
        y=cols,
        colorscale=[[0, '#e8f5e9'], [1, '#dc3545']],
        showscale=False
    ))
    fig.update_layout(title='Missing Value Heatmap', template='plotly_white',
                      height=max(300, len(cols) * 20), width=700,
                      margin=dict(l=100, r=20, t=50, b=50),
                      xaxis_visible=False)
    fig = _validate_output(fig, 'missing_heatmap', 'all')
    if fig is None:
        return None
    return _plotly_to_json(fig)


def line_chart(df, x_col, y_col, title=None):
    y_data = _prepare_numeric(df[y_col], y_col)
    if y_data is None:
        return None
    x_raw = df[x_col].dropna()
    valid_idx = y_data.index.intersection(x_raw.index)
    if len(valid_idx) < 2:
        _log_error('line_chart', y_col, f'Need at least 2 paired points, got {len(valid_idx)}')
        return None
    x_vals = x_raw.loc[valid_idx].astype(str).tolist()
    y_vals = y_data.loc[valid_idx].tolist()
    fig = go.Figure(data=[go.Scatter(x=x_vals, y=y_vals, mode='lines+markers', name=y_col,
                                      line=dict(color='#0d6efd', width=1.5))])
    fig.update_layout(title=title or f'{y_col} over {x_col}', template='plotly_white', height=400,
                      margin=dict(l=50, r=20, t=50, b=50))
    fig = _validate_output(fig, 'line_chart', y_col)
    if fig is None:
        return None
    return _plotly_to_json(fig)


def bar_chart(freq_dict, title, filename='bar_chart'):
    if not freq_dict:
        _log_error('bar_chart', filename, 'Empty frequency dictionary')
        return None
    keys = [str(k) for k in freq_dict.keys()]
    vals = []
    for v in freq_dict.values():
        try:
            vals.append(float(v))
        except (ValueError, TypeError):
            vals.append(0)
    if len(keys) == 0:
        _log_error('bar_chart', filename, 'No keys after conversion')
        return None
    fig = go.Figure(data=[go.Bar(x=keys, y=vals,
                                  marker_color='#198754', text=vals, textposition='outside')])
    fig.update_layout(title=title, template='plotly_white', height=400,
                      margin=dict(l=50, r=20, t=50, b=80))
    fig = _validate_output(fig, 'bar_chart', filename)
    if fig is None:
        return None
    return _plotly_to_json(fig)


def pie_chart(freq_dict, title, filename='pie_chart'):
    if not freq_dict:
        _log_error('pie_chart', filename, 'Empty frequency dictionary')
        return None
    labels = [str(k) for k in freq_dict.keys()]
    values = []
    for v in freq_dict.values():
        try:
            values.append(float(v))
        except (ValueError, TypeError):
            values.append(0)
    if len(labels) == 0:
        _log_error('pie_chart', filename, 'No labels after conversion')
        return None
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
    fig.update_layout(title=title, template='plotly_white', height=400)
    fig = _validate_output(fig, 'pie_chart', filename)
    if fig is None:
        return None
    return _plotly_to_json(fig)


def _prepare_datetime(series, column_name=""):
    try:
        converted = pd.to_datetime(
            series,
            format="mixed",
            errors="coerce",
            utc=True
        )
        converted = converted.dt.tz_localize(None)
        converted = converted.dropna()
        if converted.empty:
            _log_error("prepare_datetime", column_name, "No valid datetime values")
            return None
        return converted
    except Exception as e:
        _log_error("prepare_datetime", column_name, f"Conversion failed: {e}")
        return None


def trend_chart(df, date_col, value_col):
    y_data = _prepare_numeric(df[value_col], value_col)
    if y_data is None:
        return None
    dt_index = _prepare_datetime(df[date_col], date_col)
    if dt_index is None:
        _log_error('trend_chart', value_col, f'Could not parse date column: {date_col}')
        return None
    common = y_data.index.intersection(dt_index.index)
    if len(common) < 2:
        _log_error('trend_chart', value_col, f'Need at least 2 paired date-value points, got {len(common)}')
        return None
    x_vals = dt_index.loc[common].sort_values()
    y_vals = y_data.loc[x_vals.index]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines+markers',
                              name=value_col, line=dict(color='#0d6efd', width=2)))
    fig.update_layout(title=f'Trend — {value_col}', xaxis_title='Date', yaxis_title=value_col,
                      template='plotly_white', height=400, margin=dict(l=50, r=20, t=50, b=50))
    fig = _validate_output(fig, 'trend_chart', value_col)
    if fig is None:
        return None
    return _plotly_to_json(fig)


def rolling_average_chart(df, date_col, value_col, window):
    y_data = _prepare_numeric(df[value_col], value_col)
    if y_data is None:
        return None
    dt_index = _prepare_datetime(df[date_col], date_col)
    if dt_index is None:
        _log_error('rolling_average_chart', value_col, f'Could not parse date column: {date_col}')
        return None
    common = y_data.index.intersection(dt_index.index)
    if len(common) < window:
        _log_error('rolling_average_chart', value_col,
                   f'Need at least {window} paired points, got {len(common)}')
        return None
    x_vals = dt_index.loc[common].sort_values()
    y_vals = y_data.loc[x_vals.index]
    rolling_vals = y_vals.rolling(window=window, min_periods=1).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals,
                              mode='lines', name='Original',
                              line=dict(color='#adb5bd', width=1)))
    fig.add_trace(go.Scatter(x=x_vals, y=rolling_vals,
                              mode='lines', name=f'{window}-Period Rolling Avg',
                              line=dict(color='#dc3545', width=2)))
    fig.update_layout(title=f'Trend with {window}-Period Rolling Average',
                      xaxis_title='Date', yaxis_title=value_col,
                      template='plotly_white', height=400,
                      margin=dict(l=50, r=20, t=50, b=50))
    fig = _validate_output(fig, 'rolling_average_chart', value_col)
    if fig is None:
        return None
    return _plotly_to_json(fig)
