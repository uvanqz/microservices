from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from metrics_middleware import PrometheusMetricsMiddleware

app = FastAPI()

app.add_middleware(PrometheusMetricsMiddleware)

# Модель для приёма данных
class ReverseRequest(BaseModel):
    text: str

# Эндпоинт для реверса строки
@app.post("/")
async def reverse_text(request_data: ReverseRequest):
    reversed_message = request_data.text[::-1]  # Переворачиваем строку
    return {"reversed_result": reversed_message}

# Эндпоинт для метрик
@app.get("/metrics")
async def metrics():
    """
    Эндпоинт для генерации метрик в формате Prometheus
    """
    metrics_data = generate_latest()  # Генерация метрик
    return Response(content=metrics_data, media_type=CONTENT_TYPE_LATEST)
