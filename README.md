# AI381 Lab 2 – Containerized Churn Prediction API

Dr. Tariq Al-Omari · AI381 Machine Learning Operations · JUST · Fall 2026/27

## Project Overview

This project packages a machine learning churn prediction model as a FastAPI service and runs it inside a Docker container.

The model uses customer information to predict the probability of customer churn.

## Tech Stack

- Python
- FastAPI
- Scikit-learn
- Pandas
- Docker
- Pytest
- GitHub Actions
- Trivy

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks API health |
| POST | `/predict` | Returns churn probability |

## Run with Docker

Build the Docker image:

```bash
docker build -t ai381-churn-api:latest .
```

Run the container:

```bash
docker run -d --name ai381-churn-api -p 8001:8000 ai381-churn-api:latest
```

Open the health endpoint:

```bash
curl http://localhost:8001/health
```

Test a prediction:

```bash
curl -X POST http://localhost:8001/predict \
-H "Content-Type: application/json" \
-d @sample_request.json
```

## Run Tests

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the test suite:

```bash
python -m pytest -v
```

## Project Structure

```text
AI381-Lab2/
├── src/
│   ├── app/
│   │   └── main.py
│   └── train/
│       └── train.py
├── tests/
│   └── test_api.py
├── model.joblib
├── churn_v2.csv
├── sample_request.json
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
└── README.md
```

## Docker Security

- Multi-stage Docker build
- Non-root runtime user
- Docker HEALTHCHECK
- Pinned Python base image version

## CI/CD

GitHub Actions will run linting and automated tests, build the Docker image, scan it using Trivy, and publish it to GitHub Container Registry (GHCR).

## Author

Leen Banat  
Jordan University of Science and Technology (JUST)

