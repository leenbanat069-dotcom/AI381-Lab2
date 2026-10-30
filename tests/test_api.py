from fastapi.testclient import TestClient

from src.app.main import app, model

client = TestClient(app)

VALID_CUSTOMER = {
    "tenure_months": 18,
    "monthly_fee": 75.0,
    "contract": "one-year",
    "internet_service": "fiber",
    "support_calls": 1,
}


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_returns_probability():
    response = client.post("/predict", json=VALID_CUSTOMER)
    assert response.status_code == 200

    result = response.json()
    assert "churn_probability" in result
    assert 0.0 <= result["churn_probability"] <= 1.0


def test_model_is_loaded():
    assert model is not None
    assert hasattr(model, "predict_proba")


def test_invalid_input_is_rejected():
    invalid_customer = {
        **VALID_CUSTOMER,
        "tenure_months": -1,
    }
    response = client.post("/predict", json=invalid_customer)
    assert response.status_code == 422


def test_prediction_is_deterministic():
    first = client.post("/predict", json=VALID_CUSTOMER)
    second = client.post("/predict", json=VALID_CUSTOMER)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()


def test_missing_field_is_rejected():
    customer = VALID_CUSTOMER.copy()
    del customer["contract"]

    response = client.post("/predict", json=customer)
    assert response.status_code == 422
