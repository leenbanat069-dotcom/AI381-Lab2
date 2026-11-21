import json
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "artifacts" / "model.joblib"
METADATA_PATH = BASE_DIR / "artifacts" / "metadata.json"
metadata = json.loads(METADATA_PATH.read_text())
FEATURES = [
    "tenure_months",
    "monthly_charges",
    "support_calls",
    "contract",
    "internet_service",
]

app = FastAPI(title="AI381 Lab 3 Churn API")
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
    return {
        "status": "ok",
        "model_version": metadata["model_version"],
        "model": metadata["model"],
        "mlflow_run_id": metadata["mlflow_run_id"],
    }


@app.post("/predict")
def predict(customer: CustomerInput):
    data = customer.model_dump()

    # The API accepts the Lab 2 field name.
    # The Lab 3 model uses the normalized schema name.
    data["monthly_charges"] = data.pop("monthly_fee")

    X = pd.DataFrame([[data[name] for name in FEATURES]], columns=FEATURES)
    probability = float(model.predict_proba(X)[0, 1])

    return {"churn_probability": round(probability, 3)}


