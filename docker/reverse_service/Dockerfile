FROM python:3.12-slim
WORKDIR /app
RUN pip install "fastapi[standard]" httpx pydantic-settings prometheus_client
COPY reverse.py /app
COPY metrics_middleware.py /app