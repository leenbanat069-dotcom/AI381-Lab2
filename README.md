##AI381 Lab 2 – Containerized Churn Prediction API

Dr. Tariq Al-Omari · AI381 Machine Learning Operations · JUST · Fall 2026/27

##Project Overview

This project packages a machine learning churn prediction model as a FastAPI service and runs it inside a Docker container.

The model uses customer information to predict the probability of customer churn.

##Tech Stack

* Python
* FastAPI
* Scikit-learn
* Pandas
* Docker
* Pytest
* GitHub Actions
* Trivy

##API Endpoints

Method	Endpoint	Description
GET	/health	Checks API health
POST	/predict	Returns churn probability

##Run with Docker

Build the Docker image:

docker build -t ai381-churn-api:latest .

##Run the container:

docker run -d --name ai381-churn-api -p 8001:8000 ai381-churn-api:latest

##Check the health endpoint:

curl http://localhost:8001/health

##Test a prediction:

curl -X POST http://localhost:8001/predict \
-H "Content-Type: application/json" \
-d @sample_request.json

##Run Tests

Install development dependencies:

pip install -r requirements-dev.txt

##Run the test suite:

python -m pytest -v

##Project Structure

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

##Docker Security

* Multi-stage Docker build
* Non-root runtime user
* Docker HEALTHCHECK
* Pinned Python base image version
* Updated Python dependencies
* Trivy vulnerability scanning

##CI/CD Pipeline

GitHub Actions automates the following steps:

1. Runs Ruff linting.
2. Executes automated tests using Pytest.
3. Builds the Docker image.
4. Scans the image for vulnerabilities using Trivy.
5. Publishes the image to GitHub Container Registry (GHCR).

The Docker image is scanned for HIGH and CRITICAL vulnerabilities before publishing.

##Published Docker Image

Registry: GitHub Container Registry (GHCR)

- Image: ghcr.io/leenbanat069-dotcom/ai381-lab2

- Image digest: `sha256:551acb5d52c3422afc91010ccc284d61870a386a7467aad16600e1d1d8fef512`
Author
## Running the Docker Container

Pull the published image:

```bash
docker pull ghcr.io/leenbanat069-dotcom/ai381-lab2

Leen Banat
Jordan University of Science and Technology (JUST)




