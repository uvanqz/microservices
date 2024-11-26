from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from metrics_middleware import MetricsMiddleware

app = FastAPI()

# Добавление кастомного middleware для сбора метрик
app.add_middleware(MetricsMiddleware)

# Модель данных для POST-запроса
class MessageRequest(BaseModel):
    message: str  # Сообщение, которое будет передано в запросе

# Эндпоинт для обработки POST-запроса
@app.post("/process")
async def process_message(request: MessageRequest):
    """
    Этот эндпоинт принимает строку в теле запроса
    и возвращает первые 5 символов из нее.
    """
    processed_message = request.message[:5]  # Берем первые 5 символов из сообщения
    return {"result": processed_message}

# Эндпоинт для сбора метрик приложения
@app.get("/metrics")
async def get_metrics():
    """
    Эндпоинт для получения метрик приложения в формате Prometheus.
    """
    metrics_data = generate_latest()  # Генерация метрик
    return Response(content=metrics_data, media_type=CONTENT_TYPE_LATEST)
