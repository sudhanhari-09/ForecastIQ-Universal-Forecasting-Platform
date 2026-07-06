<div align="center">

# ForecastIQ – Universal AI Forecasting Platform

**An end-to-end AI-powered forecasting platform for time-series data across any domain.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-green)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)]()

</div>

---

## Project Overview

ForecastIQ is a comprehensive, end-to-end AI-powered forecasting platform capable of handling multiple time-series datasets including weather, stock, finance, sales, energy, IoT, and custom datasets. It provides a complete guided workflow from data upload to forecast report generation, with automatic and manual modes at every step.

Built with **Python** and **Flask** on the backend and **Bootstrap 5** on the frontend, ForecastIQ integrates traditional statistical models, machine learning regressors, and deep learning architectures — all accessible through an intuitive web interface.

---

## Key Features

### User Management
- **User Authentication** — Secure registration, login/logout with session management and Werkzeug password hashing
- **User Profile** — Profile page with activity tracking

### Dataset Management
- **Dataset Upload** — Upload CSV, XLS, XLSX files (up to 50 MB) with UUID-based secure file naming
- **Dataset Validation** — 9-point validation: missing values, duplicates, empty columns, data type classification, date detection, size analysis, and more

### Exploratory Data Analysis
- **Automatic EDA** — One-click comprehensive analysis with statistical summaries, correlation matrix, outlier detection, distribution plots, time-series decomposition, and data quality scoring
- **Manual EDA** — Select specific analyses and visualizations via checkboxes for a customized report

### Data Preprocessing
- **Automatic Preprocessing** — One-click cleaning with intelligent defaults
- **Manual Preprocessing** — Configure missing value handling (drop, mean, median, mode, ffill, bfill), outlier treatment (IQR, Z-Score), encoding (label, one-hot), scaling (standard, min-max, robust), and date feature extraction

### Forecasting Engine
- **Forecast Configuration** — Select date column, target column, frequency, and forecast horizon
- **Multiple Forecast Models** — 7 models across 3 categories (Traditional, ML, Deep Learning)
- **Automatic Best Model Selection** — Rank models by RMSE, MAE, MAPE, and R² with smart insights
- **Future Forecast Generation** — Predict future values with configurable horizon

### Reports & Export
- **Forecast Reports** — Comprehensive report dashboard with all analysis steps
- **CSV Export** — Download results as CSV
- **Excel Export** — Download results as XLSX via OpenPyXL
- **PDF Export** — Generate professional PDF reports via ReportLab
- **HTML Export** — Download EDA reports as interactive HTML
- **PKL Model Download** — Export trained models as pickle files

### Workflow & Insights
- **Workflow Tracking** — 6-step guided workflow with progress tracker and step locking
- **Intelligent Insights** — Smart observations about data quality, trends, and model performance

---

## Supported Forecast Models

### Traditional Models (Statsmodels)
| Model | Description |
|-------|-------------|
| **ARIMA** | Auto-Regressive Integrated Moving Average (order=1,1,1) |
| **SARIMA** | Seasonal ARIMA with yearly seasonality (order=1,1,1, seasonal_order=1,1,1,12) |
| **Exponential Smoothing** | Holt-Winters with additive trend and seasonality |

### Machine Learning Models
| Model | Description |
|-------|-------------|
| **Linear Regression** | Ordinary least squares linear regression |
| **Random Forest** | Random Forest regressor (100 trees, max_depth=10) |
| **XGBoost** | Gradient boosted trees (100 trees, learning_rate=0.1, max_depth=6) |

### Deep Learning Models
| Model | Description |
|-------|-------------|
| **LSTM** | Long Short-Term Memory network (50 units, Dropout 0.2, Dense 1) with early stopping |

All models are optional — missing libraries are gracefully skipped with clear error messages.

---

## Project Workflow

```
                        ┌──────────────┐
                        │    Login     │
                        └──────┬───────┘
                               │
                        ┌──────▼───────┐
                        │    Upload    │
                        │   Dataset   │
                        └──────┬───────┘
                               │
                        ┌──────▼───────┐
                        │  Validation  │
                        └──────┬───────┘
                               │
                        ┌──────▼───────┐
                        │     EDA     │
                        │ (Auto/Manual)│
                        └──────┬───────┘
                               │
                        ┌──────▼───────┐
                        │ Preprocessing│
                        │ (Auto/Manual)│
                        └──────┬───────┘
                               │
                        ┌──────▼───────┐
                        │   Forecast   │
                        │ Configuration│
                        └──────┬───────┘
                               │
                        ┌──────▼───────┐
                        │    Model    │
                        │   Training  │
                        └──────┬───────┘
                               │
                        ┌──────▼───────┐
                        │   Forecast  │
                        │   Results   │
                        └──────┬───────┘
                               │
                        ┌──────▼───────┐
                        │   Reports   │
                        └──────┬───────┘
                               │
                        ┌──────▼───────┐
                        │   Workflow  │
                        │  Completed  │
                        └──────────────┘
```

---

## Project Architecture

```
                        ┌─────────────────┐
                        │    Frontend     │
                        │  (Bootstrap 5,  │
                        │   JS, Plotly)   │
                        └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │  Flask Routes   │
                        │  (Blueprints)   │
                        └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │    Services     │
                        │ (Business Logic)│
                        └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │     Forecast    │
                        │     Engine      │
                        └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │   AI Models     │
                        │ (Statsmodels,   │
                        │  Sklearn, XGBoost, TensorFlow)│
                        └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │  SQLite Database│
                        │  (SQLAlchemy    │
                        │   ORM)          │
                        └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │    Reports      │
                        │ (CSV/XLSX/PDF/  │
                        │  HTML/PKL)      │
                        └─────────────────┘
```

---

## Technology Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| HTML5 / CSS3 | Structure and styling |
| Bootstrap 5.3 | Responsive UI framework |
| JavaScript (Vanilla) | Client-side interactivity |
| Plotly.js | Interactive charts |
| Font Awesome 6 | Icons |

### Backend
| Technology | Purpose |
|------------|---------|
| Python 3.9+ | Core programming language |
| Flask 3.x | Web framework |
| Flask-SQLAlchemy 3.x | ORM and database abstraction |
| Werkzeug | Password hashing and security |

### Machine Learning & AI
| Technology | Purpose |
|------------|---------|
| Scikit-learn | Linear Regression, Random Forest |
| XGBoost | Gradient boosted trees |
| Statsmodels | ARIMA, SARIMA, Exponential Smoothing |
| TensorFlow / Keras | LSTM deep learning |

### Data Processing & Analysis
| Technology | Purpose |
|------------|---------|
| Pandas | Data manipulation and analysis |
| NumPy | Numerical computing |
| SciPy | Scientific computing |

### Visualization
| Technology | Purpose |
|------------|---------|
| Plotly | Interactive web-based charts |
| Matplotlib | Static chart generation |

### Database
| Technology | Purpose |
|------------|---------|
| SQLite | Development database |
| SQLAlchemy ORM | Database abstraction layer |

### Reporting
| Technology | Purpose |
|------------|---------|
| ReportLab | PDF report generation |
| OpenPyXL | Excel (XLSX) export |

---

## Folder Structure

```
forecast_platform/
│
├── app.py                        # Flask application factory
├── config.py                     # Application configuration
├── database.py                   # SQLAlchemy ORM initialization
├── run.py                        # Application entry point
├── schema_sync.py                # Database schema migration utility
├── requirements.txt              # Python package dependencies
│
├── routes/                       # Route layer (Flask blueprints)
│   ├── auth.py                   # Authentication and dashboard routes
│   ├── dataset_routes.py         # Dataset upload, validation, preview
│   ├── eda.py                    # EDA (auto/manual) routes
│   ├── preprocessing.py          # Preprocessing (auto/manual) routes
│   ├── forecasting.py            # Forecasting setup and training routes
│   ├── comparison.py             # Model comparison routes
│   └── reports.py                # Report generation and workflow routes
│
├── services/                     # Service layer (business logic)
│   ├── dataset_service.py        # Dataset CRUD, preview, metadata
│   ├── validation_service.py     # Data quality checks and scoring
│   ├── eda_service.py            # Statistical analysis and EDA reports
│   ├── chart_service.py          # Plotly and Matplotlib chart generation
│   ├── preprocessing_service.py  # Data cleaning, scaling, encoding
│   ├── forecasting_service.py    # Model training and prediction (7 models)
│   ├── comparison_service.py     # Model ranking and comparison
│   ├── report_service.py         # Report generation (CSV/XLSX/PDF)
│   ├── workflow_service.py       # 6-step workflow state machine
│   ├── activity_service.py       # User activity logging
│   ├── model_download_service.py # Trained model export (PKL)
│   └── datetime_utils.py         # Date/time parsing utilities
│
├── models/                       # Data layer (SQLAlchemy models)
│   ├── user_model.py             # User accounts
│   ├── dataset_model.py          # Dataset metadata
│   ├── validation_report_model.py  # Validation results
│   ├── eda_report_model.py         # EDA analysis records
│   ├── preprocessing_report_model.py  # Preprocessing steps
│   ├── forecast_report_model.py     # Forecast model results
│   ├── comparison_report_model.py    # Model comparison results
│   ├── report_model.py              # Generated report records
│   ├── analysis_history_model.py     # Completed workflow history
│   └── activity_log_model.py         # User activity logs
│
├── utils/                        # Utility layer
│   └── file_utils.py             # File validation, UUID naming, security
│
├── templates/                    # Jinja2 HTML templates
│   ├── base.html                 # Base layout (Bootstrap 5)
│   ├── login.html                # User login
│   ├── register.html             # User registration
│   ├── dashboard.html            # Main dashboard
│   ├── profile.html              # User profile
│   ├── upload_dataset.html       # Dataset upload form
│   ├── upload_history.html       # Upload history list
│   ├── dataset_preview.html      # Dataset detail and preview
│   ├── validation_report.html    # Validation results
│   ├── validation_dashboard.html # Validation dashboard
│   ├── eda_mode.html             # EDA mode selection
│   ├── manual_eda.html           # Manual EDA configuration
│   ├── eda_dashboard.html        # EDA results dashboard
│   ├── eda_summary.html          # EDA summary view
│   ├── eda_charts.html           # EDA chart gallery
│   ├── preprocessing_mode.html   # Preprocessing mode selection
│   ├── manual_preprocessing.html # Manual preprocessing config
│   ├── preprocessing_dashboard.html # Preprocessing results
│   ├── preprocessing_summary.html   # Preprocessing summary
│   ├── forecast_mode.html        # Forecasting mode selection
│   ├── forecast_setup.html       # Forecast parameter configuration
│   ├── forecast_dashboard.html   # Forecast results dashboard
│   ├── forecast_results.html     # Forecast results display
│   ├── compare_dashboard.html    # Comparison dashboard
│   ├── compare_results.html      # Comparison results
│   ├── report_view.html          # Full report view
│   ├── workflow_completed.html   # Workflow completion page
│   └── components/               # Reusable template components
│       ├── workflow_bar.html     # Workflow progress tracker
│       └── workflow_bottom_nav.html  # Navigation buttons
│
├── static/                       # Static assets
│   ├── css/style.css             # Custom styles
│   └── js/main.js                # Custom JavaScript
│
├── data/                         # Data storage
│   ├── uploads/                  # Uploaded dataset files
│   └── processed/                # Preprocessed datasets
│
├── reports/                      # Generated reports
│   └── eda_reports/              # EDA HTML reports and chart images
│
├── tests/                        # Test suite
│   ├── conftest.py               # Pytest fixtures and configuration
│   ├── test_forecasting.py       # Forecasting model tests
│   ├── test_comparison.py        # Model comparison tests
│   └── test_reports.py           # Report generation tests
│
└── instance/                     # Runtime instance data
    └── forecastiq.db             # SQLite database
```

---

## Installation Guide

### Prerequisites

- **Python 3.9+**
- **pip** (Python package manager)
- **Git**

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/forecastiq.git
cd forecastiq

# 2. Create a virtual environment (recommended)
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on macOS/Linux:
# source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Install XGBoost for gradient boosting models
pip install xgboost

# 5. (Optional) Install TensorFlow for LSTM deep learning models
pip install tensorflow

# 6. Run the application
python run.py
```

Open **http://127.0.0.1:5000** in your browser to access the platform.

### Quick Start

1. **Register** a new account
2. **Upload** a CSV or Excel dataset
3. Follow the guided 6-step **workflow**: Upload → Validation → EDA → Preprocessing → Forecasting → Reports
4. **Compare** model performance and download reports in your preferred format

---

## Screenshots

### Dashboard
> *(Screenshot of the main dashboard with statistics, recent analyses, and quick actions)*

### Validation
> *(Screenshot of validation results showing data quality score, missing values, and column types)*

### EDA
> *(Screenshot of exploratory data analysis with statistical summaries and interactive charts)*

### Preprocessing
> *(Screenshot of preprocessing configuration and results)*

### Forecast Results
> *(Screenshot of forecast predictions, actual vs predicted plots, and performance metrics)*

### Reports
> *(Screenshot of the report dashboard with download options)*

---

## Future Enhancements

- **Cloud Deployment** — Deploy to AWS, GCP, or Azure for production scalability
- **API Integration** — RESTful API for programmatic access and third-party integration
- **Docker Support** — Containerized deployment with Docker and Docker Compose
- **Model Versioning** — Track and compare different versions of trained models
- **Real-time Forecasting** — Streaming data ingestion and live forecast updates
- **PostgreSQL Support** — Production-grade database with better concurrency
- **Async Task Queue** — Celery + Redis for non-blocking model training
- **Hyperparameter Tuning** — Auto-ARIMA, GridSearch, and Bayesian optimization
- **Confidence Intervals** — Prediction intervals for all forecast models
- **Ensemble Models** — Stacking and weighted averaging of multiple models
- **Prophet Integration** — Facebook Prophet model support
- **CI/CD Pipeline** — Automated testing and deployment pipeline

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Contributors

- **ForecastIQ Development Team** — Core architecture and implementation

Contributions are welcome! Please open an issue or submit a pull request.
