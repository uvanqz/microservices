import httpx
import logging

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings, SettingsConfigDict

app = FastAPI()

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("rpc_gateway")

class AppSettings(BaseSettings):
    """
    Класс для конфигурации приложения, загружает параметры из файла .env
    """
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    REVERSE_SERVICE_URL: str = 'http://reverse:8000'
    CUT_SERVICE_URL: str = 'http://cut:8000'

# Инициализация настроек
settings = AppSettings()

# Отображение методов в адреса сервисов
service_mapping = {
    'cut': settings.CUT_SERVICE_URL,
    'reverse': settings.REVERSE_SERVICE_URL,
}

@app.post("/rpc")
async def process_rpc(request: Request):
    """
    Обработка входящих RPC-запросов, направленных к нужному сервису.
    """
    log.info("Received RPC request")
    
    # Получение данных из запроса
    rpc_data = await request.json()
    method = rpc_data.get("method")
    payload = rpc_data.get("data")
    
    # Определяем URL сервиса для обработки метода
    service_url = service_mapping.get(method)
    
    if not service_url:
        # Возвращаем ошибку, если метод не найден
        raise HTTPException(detail={"error": "Unknown method"}, status_code=status.HTTP_404_NOT_FOUND)
    
    # Выполнение запроса к соответствующему сервису
    async with httpx.AsyncClient() as client:
        response = await client.post(service_url, json=payload)
    
    return JSONResponse(content=response.json(), status_code=response.status_code)
