import uvicorn
from fastapi import FastAPI

from configs.config import settings
from db.models import migrate_tables
from pkg.controllers.role import router as role_router

if __name__ == "__main__":
    # Создание таблиц
    migrate_tables()

    # Создание роутера
    app = FastAPI()
    # Подключаем маршруты
    app.include_router(role_router)

    uvicorn.run(app, port=settings.port, host=settings.host)
