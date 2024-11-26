import time

from fastapi import Request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware

# Счётчик для количества запросов
request_counter = Counter("total_requests", "Tracks the number of incoming requests", ["http_method", "endpoint"])
# Гистограмма для измерения времени отклика
latency_histogram = Histogram("request_latency_seconds", "Tracks request latency in seconds", ["endpoint"])

class PrometheusMetricsMiddleware(BaseHTTPMiddleware):
    """
    Кастомный middleware для сбора метрик Prometheus
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        request_counter.labels(http_method=request.method, endpoint=request.url.path).inc()

        response = await call_next(request)

        latency = time.time() - start_time
        # Добавляем наблюдение о времени задержки в гистограмму
        latency_histogram.labels(endpoint=request.url.path).observe(latency)

        return response
