import uvicorn
from fastapi import FastAPI

from configs.config import settings
from pkg.controllers.homeworks import router as homeworks_router
from pkg.controllers.user import router as user_router
from pkg.controllers.auth import router as auth_router
from db.models import migrate_tables

if __name__ == "__main__":
    # Создание таблиц
    migrate_tables()

    # Создание роутера
    app = FastAPI()

    # Подключаем маршруты
    app.include_router(auth_router)
    app.include_router(homeworks_router)
    app.include_router(user_router)

    uvicorn.run(app, port=settings.port, host=settings.host)
