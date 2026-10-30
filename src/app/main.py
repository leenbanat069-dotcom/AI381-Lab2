from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

MODEL_PATH = Path(__file__).resolve().parents[2] / "model.joblib"
FEATURES = [
    "tenure_months",
    "monthly_fee",
    "support_calls",
    "contract",
    "internet_service",
]

app = FastAPI(title="AI381 Lab 2 Churn API")
model = joblib.load(MODEL_PATH)


class CustomerInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tenure_months: int = Field(ge=0)
    monthly_fee: float = Field(ge=0)
    contract: str = Field(min_length=1)
    internet_service: str = Field(min_length=1)
    support_calls: int = Field(ge=0)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(customer: CustomerInput):
    data = customer.model_dump()
    X = pd.DataFrame([[data[name] for name in FEATURES]], columns=FEATURES)
    probability = float(model.predict_proba(X)[0, 1])

    return {"churn_probability": round(probability, 3)}
