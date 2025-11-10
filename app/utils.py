from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
MODEL_DIR = APP_DIR / "model"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "loan_pipeline.joblib"
TRAIN_PATH = DATA_DIR / "train.csv"
