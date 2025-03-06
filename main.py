import uvicorn
from fastapi import FastAPI

from configs.config import settings
from db.models import migrate_tables

from pkg.controllers.default import router as default_router
from pkg.controllers.CourseController import router as courses_router
from pkg.controllers.role import router as role_router

# Создание FastAPI


if __name__ == "__main__":
    # Создание таблиц
    migrate_tables()
  
    app = FastAPI()

    # Подключаем маршруты
    app.include_router(default_router)
    app.include_router(courses_router)
    app.include_router(role_router)

    uvicorn.run(app, port=settings.port, host=settings.host)
