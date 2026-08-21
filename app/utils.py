from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = Path(__file__).resolve().parent

DATA_DIR = ROOT / "data"
MODEL_DIR = APP_DIR / "model"
REPORT_DIR = ROOT / "reports"

# Create required directories
MODEL_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Dataset
TRAIN_PATH = DATA_DIR / "train.csv"

# Model
MODEL_PATH = MODEL_DIR / "loan_pipeline.joblib"

# Reports
EDA_REPORT_PATH = REPORT_DIR / "eda_report.txt"
MODEL_REPORT_PATH = REPORT_DIR / "model_summary.txt"
METRICS_REPORT_PATH = REPORT_DIR / "metrics.txt"
CROSS_VALIDATION_REPORT_PATH = REPORT_DIR / "cross_validation.txt"
FEATURE_IMPORTANCE_PATH = REPORT_DIR / "feature_importance.csv"
FEATURE_IMPORTANCE_IMAGE_PATH = REPORT_DIR / "feature_importance.png"

SHAP_SUMMARY_PATH = REPORT_DIR / "shap_summary.png"
SHAP_BAR_PATH = REPORT_DIR / "shap_bar.png"
CONFUSION_MATRIX_PATH = REPORT_DIR / "confusion_matrix.png"
ROC_CURVE_PATH = REPORT_DIR / "roc_curve.png"
