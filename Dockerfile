# Stage 1: install dependencies
FROM python:3.12.15-slim-trixie AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: runtime image
FROM python:3.12.15-slim-trixie AS runtime

ARG GIT_SHA=local

LABEL org.opencontainers.image.title="AI381 Churn API" \
      org.opencontainers.image.description="AI381 Lab 3 Champion Model API" \
      org.opencontainers.image.revision="${GIT_SHA}"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 10001 app

WORKDIR /app

COPY --from=builder /install /usr/local
COPY src/ ./src/
COPY artifacts/ ./artifacts/

# Ensure the champion exists and attach the image's commit SHA.
RUN test -f artifacts/model.joblib \
    && test -f artifacts/metadata.json \
    && python -c "import json; p='artifacts/metadata.json'; m=json.load(open(p)); m['model_version']='${GIT_SHA}'[:7]; json.dump(m,open(p,'w'),indent=2)"

USER 10001

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=3s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=2)"]

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]


