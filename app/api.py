from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib, pandas as pd
from app.schema import LoanApplication, PredictionOut
from app.utils import TRAIN_PATH, MODEL_PATH

app = FastAPI(title="Loan Eligibility API", version="1.0")

# allow browser apps (like Streamlit) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# load trained pipeline once
pipeline = joblib.load(MODEL_PATH)

@app.get("/")
def root():
    return {"status": "ok", "msg": "Loan Eligibility API is running."}

@app.head("/")
def head_root():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionOut)
def predict(payload: LoanApplication):
    df = pd.DataFrame([payload.dict()])
    prob = float(pipeline.predict_proba(df)[:, 1][0])
    pred = bool(prob >= 0.5)
    return {"approved": pred, "probability": prob}
