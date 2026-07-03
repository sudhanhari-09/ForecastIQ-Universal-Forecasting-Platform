# ForecastIQ — Universal Forecasting Platform

A web-based time series forecasting platform built with Flask. Users can upload datasets, perform automated data validation, exploratory data analysis (EDA), data preprocessing, train multiple forecasting models, compare model performance, and generate reports through a guided 6-step workflow.

---

## Features

### Phase 1 — Authentication
- User registration with server-side validation
- Login/logout with session management
- Werkzeug password hashing (pbkdf2:sha256)
- Protected routes with `@login_required` decorator
- User profile page (read-only)

### Phase 2 — Dataset Upload & Validation
- Upload CSV, XLS, XLSX files (max 50MB)
- UUID-based file renaming for security
- Dataset preview with paginated data table
- Upload history with status
- 9 validation checks:
  - Missing value analysis (count + percentage)
  - Duplicate row detection
  - Empty column detection
  - Duplicate column detection
  - Data type classification (numeric, categorical, date, text)
  - Date column auto-detection
  - Dataset size analysis

### Phase 3 — EDA (Dual Mode)

**Automatic EDA:**
- Dataset overview (rows, columns, memory usage)
- Statistical summary (mean, median, mode, std, variance, min, max, quartiles, IQR, skewness, kurtosis)
- Missing value analysis
- Correlation matrix + heatmap
- Outlier detection (IQR + Z-Score)
- Distribution analysis (histograms, boxplots, density plots)
- Categorical analysis (frequency, bar charts, pie charts)
- Time series analysis (trend, date range, frequency)
- Missing value heatmap
- Rolling average chart
- Feature insights (potential targets, high correlations, outlier-prone columns)
- Interactive Plotly charts + static Matplotlib images
- HTML report generation with embedded images
- Data quality score computation
- Smart insights generation

**Manual EDA:**
- Select specific statistics, analyses, and visualizations via checkboxes
- Generate only what is needed

### Phase 4 — Data Preprocessing
- Dual mode: **Automatic** (one-click) or **Manual** (custom configuration)
- Missing value handling: drop, mean, median, mode, forward fill, backward fill
- Outlier treatment: IQR (capping), Z-Score (capping)
- Encoding: label encoding, one-hot encoding
- Scaling: standard scaler, min-max scaler, robust scaler
- Date feature extraction (year, month, day, week, quarter, dayofweek)
- Processed dataset download (CSV/XLSX)

### Phase 5 — Forecasting Engine
- 7 forecasting models across 3 categories:
  - **Traditional:** ARIMA, SARIMA, ExponentialSmoothing (Holt-Winters)
  - **Machine Learning:** Linear Regression, Random Forest, XGBoost
  - **Deep Learning:** LSTM (TensorFlow/Keras)
- Automated time series detection (date column + frequency)
- Automated target column detection
- Date feature engineering for ML models
- Train/test split evaluation
- Performance metrics: MAE, RMSE, MAPE, R²
- Future period forecasting (configurable horizon, default 30)
- Model-specific parameter display
- Conditional imports (graceful fallback if libraries missing)
- Row-index fallback when no date column found
- Forecast CSV download

### Phase 6 — Model Comparison
- Side-by-side ranking of all trained models
- Performance metrics table (MAE, RMSE, MAPE, R²)
- Ranking by RMSE with explanatory reasons
- Smart insights (trend direction, consistency, variance, speed)
- Interactive Plotly bar charts (RMSE, MAE, MAPE, R², Training Time)
- Best model explanation with runner-up comparison
- Download comparison results (CSV/XLSX/PDF via ReportLab)

### Phase 7 — Reports & Workflow Completion
- Full report dashboard:
  - Dataset summary (name, rows, columns, upload date)
  - Validation summary
  - EDA summary (mode, charts, data quality score)
  - Preprocessing summary (methods applied)
  - Forecast summary (best model, horizon, target column)
  - Comparison summary (ranked models with metrics)
  - Smart insights
- Download reports (CSV/XLSX/PDF)
- Workflow completion page with summary stats
- Analysis history tracking per user
- Dashboard with stats, recent analyses, best models

### Workflow Management
- 6-step guided workflow: Upload → Validation → EDA → Preprocessing → Forecasting → Reports
- Workflow tracker showing progress
- Steps are locked until prerequisites are completed
- Navigation buttons to move forward/backward

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    FLASK APPLICATION                          │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│   Application Layer                                          │
│   ├── app.py                  (App Factory)                  │
│   ├── config.py               (Configuration)                │
│   ├── database.py             (SQLAlchemy init)              │
│   └── run.py                  (Entry point)                  │
│                                                               │
│   Route Layer (Blueprint-based)                               │
│   ├── routes/auth.py          (Authentication + dashboard)   │
│   ├── routes/dataset_routes.py (Upload, validate, preview)   │
│   ├── routes/eda.py           (EDA auto/manual + reports)    │
│   ├── routes/preprocessing.py (Preprocessing auto/manual)    │
│   ├── routes/forecasting.py   (Forecasting setup + training) │
│   ├── routes/comparison.py    (Model comparison)             │
│   └── routes/reports.py       (Reports + workflow complete)  │
│                                                               │
│   Service Layer (Business Logic)                              │
│   ├── services/dataset_service.py                             │
│   ├── services/validation_service.py                          │
│   ├── services/eda_service.py                                 │
│   ├── services/chart_service.py   (Plotly + Matplotlib)      │
│   ├── services/preprocessing_service.py                       │
│   ├── services/forecasting_service.py  (All model training)  │
│   ├── services/comparison_service.py                         │
│   ├── services/report_service.py                             │
│   ├── services/workflow_service.py                           │
│   └── services/activity_service.py                           │
│                                                               │
│   Data Layer                                                  │
│   ├── models/ (10 models)                                     │
│   └── instance/forecastiq.db (SQLite)                         │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

## Folder Structure

```
forecast_platform/
├── app.py                      # Flask app factory
├── config.py                   # Configuration
├── database.py                 # SQLAlchemy ORM init
├── run.py                      # Application entry point
├── schema_sync.py              # Auto schema migration
├── requirements.txt            # Python dependencies
│
├── routes/
│   ├── __init__.py
│   ├── auth.py                 # Auth + dashboard
│   ├── dataset_routes.py       # Dataset management
│   ├── eda.py                  # EDA engine
│   ├── preprocessing.py        # Preprocessing
│   ├── forecasting.py          # Forecasting
│   ├── comparison.py           # Model comparison
│   └── reports.py              # Reports + workflow complete
│
├── services/
│   ├── __init__.py
│   ├── dataset_service.py      # Upload, preview, CRUD
│   ├── validation_service.py   # Data quality checks
│   ├── eda_service.py          # EDA computation + HTML report
│   ├── chart_service.py        # Plotly + Matplotlib charts
│   ├── preprocessing_service.py # Missing values, scaling, encoding
│   ├── forecasting_service.py  # Model training (7 models)
│   ├── comparison_service.py   # Model ranking + insights
│   ├── report_service.py       # Report generation (CSV/XLSX/PDF)
│   ├── workflow_service.py     # 6-step workflow state machine
│   └── activity_service.py     # Activity logging
│
├── models/
│   ├── __init__.py
│   ├── user_model.py
│   ├── dataset_model.py
│   ├── validation_report_model.py
│   ├── eda_report_model.py
│   ├── preprocessing_report_model.py
│   ├── forecast_report_model.py
│   ├── comparison_report_model.py
│   ├── report_model.py
│   ├── analysis_history_model.py
│   └── activity_log_model.py
│
├── utils/
│   └── file_utils.py           # File validation, UUID naming
│
├── templates/
│   ├── base.html               # Bootstrap 5 base template
│   ├── login.html              # User login
│   ├── register.html           # User registration
│   ├── dashboard.html          # Main dashboard
│   ├── profile.html            # User profile
│   ├── upload_dataset.html     # Dataset upload form
│   ├── upload_history.html     # Upload history list
│   ├── dataset_preview.html    # Dataset detail + preview
│   ├── validation_report.html  # Validation results
│   ├── validation_dashboard.html # Validation dashboard
│   ├── eda_mode.html           # EDA mode selection
│   ├── manual_eda.html         # Manual EDA configuration
│   ├── eda_dashboard.html      # EDA results dashboard
│   ├── eda_summary.html        # EDA summary
│   ├── eda_charts.html         # EDA chart gallery
│   ├── preprocessing_mode.html # Preprocessing mode selection
│   ├── manual_preprocessing.html # Manual preprocessing config
│   ├── preprocessing_dashboard.html # Preprocessing results
│   ├── preprocessing_summary.html   # Preprocessing summary
│   ├── forecast_mode.html      # Forecasting mode
│   ├── forecast_setup.html     # Forecast parameter config
│   ├── forecast_dashboard.html # Forecast results dashboard
│   ├── forecast_results.html   # Forecast results display
│   ├── compare_dashboard.html  # Comparison dashboard
│   ├── compare_results.html    # Comparison results
│   ├── report_view.html        # Full report view
│   └── workflow_completed.html # Workflow completion page
│
├── static/
│   ├── css/style.css           # Custom styles
│   └── js/main.js              # Custom JavaScript
│
├── data/
│   ├── uploads/                # Uploaded dataset files
│   └── processed/              # Preprocessed datasets
│
├── reports/
│   └── eda_reports/            # Generated EDA reports + chart images
│
├── tests/
│   ├── conftest.py             # Pytest fixtures
│   ├── test_forecasting.py     # Forecasting tests
│   ├── test_comparison.py      # Comparison tests
│   └── test_reports.py         # Reports tests
│
└── instance/
    └── forecastiq.db           # SQLite database
```

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap 5.3, Font Awesome 6, Plotly.js |
| **Backend** | Python 3, Flask 3.x, Flask-SQLAlchemy 3.x |
| **Database** | SQLite (development), SQLAlchemy ORM |
| **Data Processing** | Pandas, NumPy, SciPy |
| **Time Series** | Statsmodels (ARIMA, SARIMA, ExponentialSmoothing) |
| **Machine Learning** | Scikit-learn (LinearRegression, RandomForest), XGBoost |
| **Deep Learning** | TensorFlow/Keras (LSTM) |
| **Visualization** | Plotly (interactive), Matplotlib (static) |
| **Reporting** | ReportLab (PDF), OpenPyXL (Excel) |
| **Testing** | Pytest |
| **Security** | Werkzeug password hashing, UUID file renaming |

## Database Tables

| Table | Purpose |
|-------|---------|
| `users` | User accounts (id, username, email, password_hash, created_at) |
| `datasets` | Uploaded file metadata (file_name, file_path, file_size, rows, columns, workflow_step) |
| `validation_reports` | Validation results (missing values, duplicates, column types, data quality) |
| `eda_reports` | EDA analysis records (mode, chart count, report path) |
| `preprocessing_reports` | Preprocessing steps (mode, steps applied, original/processed shapes) |
| `forecast_reports` | Forecast model results (model name, horizon, metrics) |
| `comparison_reports` | Model comparison results (best model, ranking, metrics) |
| `reports` | Generated report records |
| `analysis_history` | Completed workflow history per user |
| `activity_logs` | User activity tracking (actions, timestamps) |

## Installation

### Prerequisites
- Python 3.9+
- pip

### Setup

```bash
# Navigate to the project
cd forecast_platform

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

Open **http://127.0.0.1:5000** in your browser.

### Optional Dependencies

For XGBoost:
```bash
pip install xgboost
```

For LSTM (deep learning):
```bash
pip install tensorflow
```

For PDF report generation (ReportLab is included in requirements.txt).

## Usage

### Workflow

```
Register → Login → Upload Dataset
    → Validation (auto)
    → EDA (Auto / Manual)
    → Preprocessing (Auto / Manual)
    → Forecasting (select model(s), train, view results)
    → Comparison (rank models, view metrics, charts)
    → Reports Dashboard (download CSV/XLSX/PDF)
    → Workflow Completed (summary + action cards)
```

Each step has a workflow tracker showing progress, with navigation buttons to move forward/backward. Steps are locked until prerequisites are completed.

## Machine Learning Models

### Traditional Time Series (statsmodels)
| Model | Description | Dependencies |
|-------|-------------|-------------|
| **ARIMA** | Auto-Regressive Integrated Moving Average (order=1,1,1) | statsmodels |
| **SARIMA** | Seasonal ARIMA (order=1,1,1, seasonal_order=1,1,1,12) | statsmodels |
| **ExponentialSmoothing** | Holt-Winters with additive trend and seasonality | statsmodels |

### Machine Learning (scikit-learn / XGBoost)
| Model | Description | Dependencies |
|-------|-------------|-------------|
| **LinearRegression** | Ordinary least squares linear regression | scikit-learn |
| **RandomForest** | Random Forest regressor (100 trees, max_depth=10) | scikit-learn |
| **XGBoost** | Gradient boosted trees (100 trees, lr=0.1, max_depth=6) | xgboost |

### Deep Learning (TensorFlow/Keras)
| Model | Description | Dependencies |
|-------|-------------|-------------|
| **LSTM** | LSTM(50) → Dropout(0.2) → Dense(1) with early stopping | tensorflow |

All models are optional — if a library is not installed, the corresponding model is skipped with a clear error message.

### Performance Metrics
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- MAPE (Mean Absolute Percentage Error)
- R² (Coefficient of Determination)

## Supported Dataset Types

| Feature | Details |
|---------|---------|
| **File Formats** | CSV (.csv), Excel (.xls, .xlsx) |
| **Max File Size** | 50 MB |
| **Date Detection** | Automatic — datetime columns, string dates, numeric timestamps (Unix s/ms/ns) |
| **Target Detection** | Automatic — highest variance numeric column |
| **Column Types** | Numeric, categorical, date, text, boolean |
| **Encoding** | UTF-8, ISO-8859-1 fallback |

## Screenshots

*(Screenshots to be added)*

## API Routes

### Authentication
| Route | Methods | Description |
|-------|---------|-------------|
| `/` | GET | Redirect to login/dashboard |
| `/login` | GET, POST | User login |
| `/register` | GET, POST | User registration |
| `/logout` | GET | Logout |
| `/dashboard` | GET | User dashboard |
| `/profile` | GET | User profile |

### Datasets
| Route | Methods | Description |
|-------|---------|-------------|
| `/upload` | GET, POST | Upload dataset |
| `/datasets` | GET | Upload history |
| `/dataset/<id>` | GET | Dataset detail + preview |
| `/dataset/<id>/preview` | GET | Full preview (50 rows) |
| `/dataset/<id>/validate` | POST | Run validation |
| `/dataset/<id>/validation` | GET | Validation dashboard |
| `/validation-report/<id>` | GET | View validation report |
| `/dataset/<id>/delete` | POST | Delete dataset |

### EDA
| Route | Methods | Description |
|-------|---------|-------------|
| `/eda-mode/<id>` | GET | EDA mode selection |
| `/eda-auto/<id>` | POST | Run automatic EDA |
| `/eda-manual/<id>` | GET, POST | Run manual EDA |
| `/eda-dashboard/<id>` | GET | EDA results dashboard |
| `/generate-eda-report/<id>` | POST | Generate HTML report |
| `/download-eda-report/<id>` | GET | Download HTML report |

### Preprocessing
| Route | Methods | Description |
|-------|---------|-------------|
| `/preprocessing-mode/<id>` | GET | Preprocessing mode selection |
| `/preprocessing-auto/<id>` | POST | Run automatic preprocessing |
| `/preprocessing-manual/<id>` | GET, POST | Run manual preprocessing |
| `/preprocessing-dashboard/<id>` | GET | Preprocessing results |
| `/preprocessing-summary/<id>` | GET | Preprocessing summary |
| `/download-processed/<id>` | GET | Download processed dataset |

### Forecasting
| Route | Methods | Description |
|-------|---------|-------------|
| `/forecasting/setup/<id>` | GET | Forecast parameter setup |
| `/forecasting/train/<id>` | POST | Train models |
| `/forecasting/results/<id>` | GET | Forecast results |
| `/forecasting/dashboard/<id>` | GET | Forecast dashboard |
| `/forecasting/download/<id>` | GET | Download forecast CSV |

### Comparison
| Route | Methods | Description |
|-------|---------|-------------|
| `/compare/<id>` | GET, POST | Run model comparison |
| `/compare/results/<id>` | GET | Comparison results |
| `/compare/api/model/<id>/<name>` | GET | Model actual vs predicted data |
| `/compare/download/<id>/<format>` | GET | Download comparison (CSV/XLSX/PDF) |

### Reports
| Route | Methods | Description |
|-------|---------|-------------|
| `/reports/<id>` | GET | Full report dashboard |
| `/workflow/completed/<id>` | GET | Workflow completion page |
| `/reports/download/<id>/<format>` | GET | Download report (CSV/XLSX/PDF) |

## Testing

```bash
# Run all tests
python -m pytest

# Run specific test files
python -m pytest tests/test_reports.py -v
python -m pytest tests/test_comparison.py -v
python -m pytest tests/test_forecasting.py -v
```

## Known Limitations

- **Database**: SQLite only (not suitable for production concurrency)
- **Prophet**: Listed in requirements but no Prophet model implementation exists in the codebase
- **Ensemble Model**: Referenced in architecture docs but not implemented
- **Templates**: `compare_dashboard.html` exists in the template directory but the compare route redirects directly to results (the dashboard template is unused)
- **EDA Summary/Charts**: `/eda-summary/<id>` and `/eda-charts/<id>` routes redirect to the EDA dashboard rather than serving standalone pages
- **Forecast Mode Page**: `/forecasting/<id>` redirects directly to the setup page (`/forecasting/setup/<id>`)
- **User Profile**: Read-only — no profile editing or password change functionality
- **No REST API**: All routes return HTML templates (no JSON API for programmatic access)
- **No Async Task Queue**: All training runs synchronously in the request thread (may timeout for large datasets)
- **No Model Persistence**: Trained models are not saved to disk (only predictions and metrics are stored)
- **Confidence Intervals**: Not calculated for forecast predictions
- **No Hyperparameter Tuning**: Models use fixed default parameters
- **CSRF Protection**: Not implemented (no Flask-WTF)
- **No Pagination**: Upload history pagination is not functional (broken in UI)
- **Minimal Test Coverage**: Only 3 test files exist covering forecasting, comparison, and reports

## Future Improvements

- PostgreSQL database support for production use
- Prophet and Ensemble model implementations
- Hyperparameter tuning (GridSearch, Auto-ARIMA)
- Asynchronous task queue (Celery + Redis) for model training
- REST API endpoints for programmatic access
- Export trained models (pickle/saved_model format)
- Confidence interval calculation for all models
- Stationarity testing (ADF test) in EDA module
- Seasonal decomposition (STL) in EDA module
- ACF/PACF plots for time series analysis
- User profile editing and password management
- Drag-and-drop file upload with preview
- Dark/light theme toggle
- Docker containerization
- CI/CD pipeline

## License

MIT

## Author

ForecastIQ Development Team
