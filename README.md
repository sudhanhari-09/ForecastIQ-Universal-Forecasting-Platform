<div align="center">

# ForecastIQ – Universal AI Forecasting Platform

**An end-to-end AI-powered forecasting platform for time-series data across any domain.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-green)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)]()
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)](https://tensorflow.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-3.x-red)](https://xgboost.readthedocs.io)

</div>

---

## Project Overview

ForecastIQ is a comprehensive, end-to-end AI-powered forecasting platform capable of handling multiple time-series datasets including weather, stock, finance, sales, energy, IoT, and custom datasets. It provides a complete guided 6-step workflow from data upload to forecast report generation, with automatic and manual modes at every step.

Built with **Python** and **Flask** on the backend and **Bootstrap 5** on the frontend, ForecastIQ integrates traditional statistical models, machine learning regressors, and deep learning architectures — all accessible through an intuitive web interface with an **AI Copilot** assistant.

---

## Features

### User Management
| Feature | Description |
|---------|-------------|
| User Authentication | Secure registration, login/logout with session management |
| User Profile | Profile page with account details |
| Activity Logging | Automatic tracking of all user actions across workflows |

### Dataset Management
| Feature | Description |
|---------|-------------|
| Dataset Upload | Upload CSV, XLS, XLSX files (up to 50 MB) with UUID-based secure file naming |
| Dataset Preview | Column-level preview with data types and sample rows |
| Upload History | Paginated, searchable, filterable dataset history with AJAX |
| Dataset Deletion | Full dataset removal with cascade cleanup |

### Validation
| Feature | Description |
|---------|-------------|
| Missing Value Detection | Per-column missing count and percentage analysis |
| Duplicate Detection | Duplicate row and duplicate column identification |
| Empty Column Detection | Columns with zero non-null values |
| Data Type Classification | Automatic detection of numeric, categorical, date, and boolean columns |
| Validation Dashboard | Visual score, issues list, recommendations, and column detail stats |

### Exploratory Data Analysis
| Feature | Description |
|---------|-------------|
| Automatic EDA | One-click comprehensive analysis with 9+ chart types |
| Manual EDA | Select specific statistics, analysis, and chart types via checkboxes |
| Statistical Summary | Count, mean, median, std, min, max, quartiles, IQR, skewness, kurtosis |
| Missing Analysis | Column-wise and overall missing value statistics |
| Correlation Analysis | Full correlation matrix with highly-correlated pair detection |
| Outlier Detection | IQR and Z-Score based outlier identification |
| Categorical Analysis | Frequency distribution, top values, unique counts |
| Time-Series Analysis | Automatic date detection, trend analysis, frequency inference |
| Data Quality Scoring | Composite quality score with letter grade (A–D) |
| Smart Insights | Auto-generated observations about data quality and patterns |
| Interactive Charts | Histograms, box plots, density plots, correlation heatmap, missing heatmap, bar charts, pie charts, trend lines, rolling averages |
| EDA Report Export | Downloadable HTML report with embedded Plotly charts |

### Preprocessing
| Feature | Description |
|---------|-------------|
| Automatic Preprocessing | One-click cleaning with intelligent defaults |
| Manual Preprocessing | Configure missing value handling (drop, mean, median, mode, ffill, bfill) |
| Outlier Treatment | IQR capping or Z-Score capping with column selection |
| Encoding | Label encoding or one-hot encoding for categorical columns |
| Scaling | Standard, Min-Max, or Robust scaling for numeric columns |
| Date Feature Extraction | Automatic extraction of year, month, day, dayofweek, quarter, etc. |
| Processed Dataset Download | Export cleaned dataset as CSV or XLSX |

### Forecasting Engine
| Feature | Description |
|---------|-------------|
| Forecast Configuration | Select date column, target column, frequency, and forecast horizon |
| Multiple Models | 7 models across 3 categories (Traditional, ML, Deep Learning) |
| Automatic Mode | Trains all models and selects the best by RMSE |
| Manual Mode | Train a specific model with custom parameters |
| Automatic Train/Test Split | Configurable test ratio (default 20%) |
| Comprehensive Metrics | MAE, RMSE, MAPE, R², SMAPE, explained variance, median absolute error, max error, prediction accuracy |
| Confidence Intervals | 95% prediction intervals for all forecasts |
| Forecast Statistics | Min, max, average, median, std, variance, range, sum |
| Error Distribution | Bucketed error analysis with frequency counts |
| Model Insights | Trend analysis, stability, volatility, seasonality detection, prediction reliability |
| Business Recommendations | Auto-generated actionable business advice based on forecast quality |
| Model Download | Export trained model as PKL with metadata, README, and requirements |
| Export Formats | CSV, Excel, PDF, HTML forecast downloads |
| All-Model Comparison | Side-by-side metrics comparison with Plotly bar charts |

### Model Comparison
| Feature | Description |
|---------|-------------|
| Automated Ranking | Models ranked by RMSE with tie-breaking by MAE and R² |
| Best Model Selection | Automatic identification with detailed explanation |
| Comparison Charts | RMSE, MAE, MAPE, R², and training time bar charts via Plotly |
| Smart Insights | Category dominance, consistency analysis, speed comparisons |
| Per-Model Detail | Access actual vs predicted data for any individual model |
| Export Formats | CSV, Excel, PDF download of comparison results |

### Reports
| Feature | Description |
|---------|-------------|
| Full Workflow Report | Comprehensive report covering all 6 workflow steps |
| Workflow Summary | Step-by-step progress with timestamps |
| Model Rankings | Ranked model table with metrics and reasons |
| Smart Insights | Auto-generated observations about the entire analysis |
| Forecast Values | Complete forecast table with periods and values |
| Export Formats | CSV, Excel (multi-sheet), PDF with professional formatting |
| Model Export | Download trained model as PKL package with dependencies |

### Dashboard
| Feature | Description |
|---------|-------------|
| Statistics Overview | Total datasets, validated count, forecast count, report count |
| Quick Actions | Upload dataset, view analytics, browse history |
| Recent Activity | Activity feed showing user actions |
| Analysis History | Recent analyses with best model, horizon, and workflow time |
| Best Models Chart | Top performing models across all analyses |

### AI Copilot
| Feature | Description |
|---------|-------------|
| Multi-Provider Support | OpenAI, Gemini, and OpenRouter providers |
| Secure API Key Storage | Encrypted API key storage using itsdangerous |
| Configurable Model | Custom model ID, temperature, and max tokens |
| Project-Aware Responses | Automatic dataset context injection |
| Workflow Awareness | Understands current workflow step and dataset state |
| Forecast Explanation | Explains RMSE, MAE, MAPE, R² in plain language |
| Report Insights | Answers questions about validation, EDA, preprocessing, and forecasts |
| Floating Chat Interface | Accessible from any page via floating action button |

---

## Complete Workflow

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
                         │ (Auto/Manual)│
                         └──────┬───────┘
                                │
                         ┌──────▼───────┐
                         │   Model     │
                         │  Comparison │
                         └──────┬───────┘
                                │
                         ┌──────▼───────┐
                         │   Reports   │
                         └──────┬───────┘
                                │
                         ┌──────▼───────┐
                         │   Workflow  │
                         │  Completed  │
                         └──────┬───────┘
                                │
                         ┌──────▼───────┐
                         │  AI Copilot  │
                         │ (Any Step)   │
                         └──────────────┘
```

---

## Dashboard Screens

| Screen | Route | Purpose |
|--------|-------|---------|
| **Main Dashboard** | `/dashboard` | Statistics overview, quick actions, recent activity, analysis history |
| **Upload Dataset** | `/upload` | File upload with name and metadata |
| **Upload History** | `/datasets` | Paginated, searchable list of all datasets |
| **Dataset Preview** | `/dataset/<id>` | Column preview, data types, sample rows |
| **Validation Dashboard** | `/dataset/<id>/validation` | Validation score, issues, recommendations, column stats |
| **EDA Mode Selection** | `/eda-mode/<id>` | Choose automatic or manual EDA |
| **Manual EDA** | `/eda-manual/<id>` | Select statistics, analysis, and chart types |
| **EDA Dashboard** | `/eda-dashboard/<id>` | Interactive charts, statistics, data quality score, insights |
| **Preprocessing Mode** | `/preprocessing-mode/<id>` | Choose automatic or manual preprocessing |
| **Manual Preprocessing** | `/preprocessing-manual/<id>` | Configure missing, outlier, encoding, scaling settings |
| **Preprocessing Dashboard** | `/preprocessing-dashboard/<id>` | Applied steps, shape changes, download processed data |
| **Forecast Setup** | `/forecasting/setup/<id>` | Select date/target columns, model, horizon |
| **Forecast Results** | `/forecasting/results/<id>` | Actual vs predicted chart, future forecast chart, metrics, insights |
| **Comparison Dashboard** | `/compare/<id>` | Model ranking, comparison charts, insights |
| **Comparison Results** | `/compare/results/<id>` | Detailed comparison view with download options |
| **Report View** | `/reports/<id>` | Full workflow report with all steps, rankings, insights |
| **Workflow Completed** | `/workflow/completed/<id>` | Workflow completion summary |
| **AI Copilot Settings** | `/ai/settings` | Configure AI provider, API key, model parameters |
| **User Profile** | `/profile` | Account details |

---

## Forecasting Models

### Traditional Models (Statsmodels)
| Model | Description | Parameters |
|-------|-------------|------------|
| **ARIMA** | Auto-Regressive Integrated Moving Average | order=(1,1,1) |
| **SARIMA** | Seasonal ARIMA with yearly seasonality | order=(1,1,1), seasonal_order=(1,1,1,12) |
| **Exponential Smoothing** | Holt-Winters with additive trend and seasonality | seasonal_periods=12 |

### Machine Learning Models (Scikit-learn / XGBoost)
| Model | Description | Parameters |
|-------|-------------|------------|
| **Linear Regression** | Ordinary least squares linear regression | Default |
| **Random Forest** | Random Forest regressor | 100 trees, max_depth=10, n_jobs=-1 |
| **XGBoost** | Gradient boosted trees | 100 trees, learning_rate=0.1, max_depth=6 |

### Deep Learning Models (TensorFlow / Keras)
| Model | Description | Architecture |
|-------|-------------|--------------|
| **LSTM** | Long Short-Term Memory network | LSTM(50) → Dropout(0.2) → Dense(1), Early Stopping |

All models are optional — missing libraries are gracefully skipped with clear error messages.

---

## Technology Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| HTML5 / CSS3 | Structure and styling |
| Bootstrap 5.3 | Responsive UI framework |
| JavaScript (Vanilla) | Client-side interactivity |
| Plotly.js 2.27 | Interactive charts |
| Font Awesome 6 | Icon library |
| Google Fonts (Inter) | Typography |

### Backend
| Technology | Purpose |
|------------|---------|
| Python 3.9+ | Core programming language |
| Flask 3.1 | Web framework |
| Flask-SQLAlchemy 3.1 | ORM and database abstraction |
| Werkzeug 3.1 | Password hashing and security |
| Jinja2 3.1 | Template engine |
| itsdangerous | API key encryption |

### Machine Learning & AI
| Technology | Purpose |
|------------|---------|
| Scikit-learn 1.9 | Linear Regression, Random Forest |
| XGBoost 3.3 | Gradient boosted trees |
| Statsmodels 0.14 | ARIMA, SARIMA, Exponential Smoothing |
| TensorFlow 2.21 / Keras 3.15 | LSTM deep learning |
| Joblib | Model serialization |

### Data Processing & Analysis
| Technology | Purpose |
|------------|---------|
| Pandas 3.0 | Data manipulation and analysis |
| NumPy 2.5 | Numerical computing |
| SciPy 1.18 | Scientific computing |
| Matplotlib 3.11 | Static chart generation |

### Visualization
| Technology | Purpose |
|------------|---------|
| Plotly 6.8 | Interactive web-based charts |

### Database
| Technology | Purpose |
|------------|---------|
| SQLite | Development database |
| SQLAlchemy ORM 2.0 | Database abstraction layer |

### AI Integration
| Technology | Purpose |
|------------|---------|
| OpenAI API | GPT model integration |
| Gemini API | Google Gemini integration |
| OpenRouter API | Multi-model provider gateway |

### Reporting
| Technology | Purpose |
|------------|---------|
| ReportLab 5.0 | PDF report generation |
| OpenPyXL 3.1 | Excel (XLSX) export |
| CSV | Tabular data export |

---

## AI Copilot

The **AI Copilot** is an intelligent conversational assistant integrated into every page of ForecastIQ.

### Provider Support

| Provider | Models | Integration |
|----------|--------|-------------|
| **OpenAI** | gpt-4o-mini, gpt-4o, gpt-4, etc. | REST API via `requests` |
| **Gemini** | gemini-pro, gemini-1.5-pro, etc. | REST API via `requests` |
| **OpenRouter** | Any LLM through unified API | REST API via `requests` |

### Capabilities

- **Project-Aware Responses** — Automatically injects dataset context (name, rows, columns, workflow step) into the system prompt
- **Dataset Understanding** — Knows about validation results, EDA statistics, preprocessing steps, forecast metrics, and comparison rankings
- **Forecast Explanation** — Explains RMSE, MAE, MAPE, R², SMAPE, and other metrics in plain language
- **Report Explanation** — Answers questions about the generated report, smart insights, and business recommendations
- **ML Assistance** — Helps users understand model selection, data quality issues, and preprocessing decisions
- **Workflow Guidance** — Suggests next steps based on current workflow progress

### Architecture

The AI Copilot uses a **system prompt** dynamically built from the user's dataset context. When the user sends a message, the system:

1. Retrieves the user's AI settings (provider, model, API key)
2. Gathers dataset context from all workflow stages (validation, EDA, preprocessing, forecasting, comparison, report)
3. Builds a comprehensive system prompt with structured data
4. Sends the conversation to the configured AI provider
5. Returns the response with context availability flags

API keys are encrypted at rest using `itsdangerous.URLSafeSerializer`.

---

## Project Architecture

```
                         ┌─────────────────────────┐
                         │       Frontend          │
                         │  (Bootstrap 5, Plotly,  │
                         │   Font Awesome, Inter)  │
                         └───────────┬─────────────┘
                                     │
                         ┌───────────▼─────────────┐
                         │     Flask Blueprints    │
                         │  auth / dataset / eda   │
                         │  preprocessing /        │
                         │  forecasting /          │
                         │  comparison / reports   │
                         │  ai                     │
                         └───────────┬─────────────┘
                                     │
                         ┌───────────▼─────────────┐
                         │       Services          │
                         │  (Business Logic)       │
                         │  dataset / validation   │
                         │  eda / chart /          │
                         │  preprocessing /        │
                         │  forecasting /          │
                         │  comparison / report    │
                         │  workflow / activity    │
                         │  model_download / ai    │
                         └───────────┬─────────────┘
                                     │
                         ┌───────────▼─────────────┐
                         │     Forecast Engine     │
                         │  ARIMA / SARIMA / ETS   │
                         │  LinearRegression / RF  │
                         │  XGBoost / LSTM         │
                         └───────────┬─────────────┘
                                     │
                         ┌───────────▼─────────────┐
                         │     AI Providers        │
                         │  OpenAI / Gemini /      │
                         │  OpenRouter             │
                         └───────────┬─────────────┘
                                     │
                         ┌───────────▼─────────────┐
                         │   SQLite Database       │
                         │  (SQLAlchemy ORM)       │
                         │  11 models              │
                         └───────────┬─────────────┘
                                     │
                         ┌───────────▼─────────────┐
                         │      Reports & Export   │
                         │  CSV / XLSX / PDF /     │
                         │  HTML / PKL             │
                         └─────────────────────────┘
```

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
│   ├── reports.py                # Report generation and workflow routes
│   └── ai.py                     # AI Copilot settings and chat routes
│
├── services/                     # Service layer (business logic)
│   ├── dataset_service.py        # Dataset CRUD, preview, metadata
│   ├── validation_service.py     # Data quality checks and scoring
│   ├── eda_service.py            # Statistical analysis and EDA reports
│   ├── chart_service.py          # Plotly chart generation
│   ├── preprocessing_service.py  # Data cleaning, scaling, encoding
│   ├── forecasting_service.py    # Model training and prediction (7 models)
│   ├── comparison_service.py     # Model ranking and comparison
│   ├── report_service.py         # Report generation (CSV/XLSX/PDF)
│   ├── workflow_service.py       # 6-step workflow state machine
│   ├── activity_service.py       # User activity logging
│   ├── model_download_service.py # Trained model export (PKL)
│   ├── ai_service.py             # AI Copilot chat and context building
│   ├── datetime_utils.py         # Date/time parsing utilities
│   └── providers/                # AI provider implementations
│       ├── openai_provider.py    # OpenAI API integration
│       ├── gemini_provider.py    # Google Gemini API integration
│       └── openrouter_provider.py # OpenRouter API integration
│
├── models/                       # Data layer (SQLAlchemy models)
│   ├── user_model.py             # User accounts
│   ├── dataset_model.py          # Dataset metadata
│   ├── validation_report_model.py # Validation results
│   ├── eda_report_model.py       # EDA analysis records
│   ├── preprocessing_report_model.py # Preprocessing steps
│   ├── forecast_report_model.py  # Forecast model results
│   ├── comparison_report_model.py # Model comparison results
│   ├── report_model.py           # Generated report records
│   ├── analysis_history_model.py # Completed workflow history
│   ├── activity_log_model.py     # User activity logs
│   └── ai_settings_model.py      # AI Copilot configuration
│
├── utils/                        # Utility layer
│   └── file_utils.py             # File validation, UUID naming, security
│
├── templates/                    # Jinja2 HTML templates
│   ├── base.html                 # Base layout (Bootstrap 5 + AI Copilot)
│   ├── login.html                # User login
│   ├── register.html             # User registration
│   ├── dashboard.html            # Main dashboard
│   ├── profile.html              # User profile
│   ├── upload_dataset.html       # Dataset upload form
│   ├── upload_history.html       # Upload history list
│   ├── _dataset_table.html       # AJAX dataset table partial
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
│   ├── forecast_mode.html        # Forecasting mode selection
│   ├── forecast_setup.html       # Forecast parameter configuration
│   ├── forecast_dashboard.html   # Forecast results dashboard
│   ├── forecast_results.html     # Forecast results display
│   ├── compare_dashboard.html    # Comparison dashboard
│   ├── compare_results.html      # Comparison results
│   ├── report_view.html          # Full report view
│   ├── workflow_completed.html   # Workflow completion page
│   ├── settings_ai.html          # AI Copilot settings
│   ├── ai_chat.html              # AI Copilot chat interface (included in base)
│   └── components/               # Reusable template components
│       ├── workflow_bar.html     # Workflow progress tracker
│       └── workflow_bottom_nav.html # Navigation buttons
│
├── static/                       # Static assets
│   ├── css/
│   │   ├── style.css             # Custom application styles
│   │   └── ai_chat.css           # AI Copilot chat styles
│   └── js/
│       ├── main.js               # Core JavaScript
│       └── ai_chat.js            # AI Copilot chat interaction
│
├── data/                         # Data storage
│   ├── uploads/                  # Uploaded dataset files
│   ├── processed/                # Preprocessed datasets
│   └── forecasts/                # Forecast results and model exports
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

# 4. Run the application
python run.py
```

Open **http://127.0.0.1:5000** in your browser to access the platform.

### Quick Start

1. **Register** a new account
2. **Upload** a CSV or Excel dataset
3. Follow the guided 6-step **workflow**: Upload → Validation → EDA → Preprocessing → Forecasting → Reports
4. **Compare** model performance and download reports in your preferred format
5. **Configure AI Copilot** in Settings to enable intelligent assistance

---

## Screenshots

### Dashboard
> *(Main dashboard with statistics, recent analyses, and quick actions)*

### Validation
> *(Validation results showing data quality score, missing values, and column types)*

### EDA
> *(Exploratory data analysis with statistical summaries and interactive charts)*

### Preprocessing
> *(Preprocessing configuration and results)*

### Forecast Results
> *(Forecast predictions, actual vs predicted plots, and performance metrics)*

### Comparison
> *(Model comparison with ranked results and metric bar charts)*

### Reports
> *(Report dashboard with download options)*

### AI Copilot
> *(Floating AI assistant with contextual dataset awareness)*

---

## Future Enhancements

- **Cloud Deployment** — Deploy to AWS, GCP, or Azure for production scalability
- **Docker Support** — Containerized deployment with Docker and Docker Compose
- **PostgreSQL Support** — Production-grade database with better concurrency
- **Async Task Queue** — Celery + Redis for non-blocking model training
- **Hyperparameter Tuning** — Auto-ARIMA, GridSearch, and Bayesian optimization
- **Ensemble Models** — Stacking and weighted averaging of multiple models
- **Prophet Integration** — Facebook Prophet model support
- **Real-time Forecasting** — Streaming data ingestion and live forecast updates
- **CI/CD Pipeline** — Automated testing and deployment pipeline
- **REST API** — Programmatic access for third-party integration

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Developed By

- Harihara Sudhan S
- Janani Boopathiraj

**ForecastIQ – Universal Forecasting Platform**
