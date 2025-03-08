import uvicorn
from fastapi import FastAPI

from configs.config import settings
from db.models import migrate_tables

from pkg.controllers.default import router as default_router
from pkg.controllers.homeworks import router as homework_router
from pkg.controllers.lesson import router as lesson_router
from pkg.controllers.CourseController import router as courses_router
from pkg.controllers.attendances import router as attendance_router
from pkg.controllers.role import router as role_router
from pkg.controllers.event import router as event_router

app = FastAPI()

# Создание таблиц
migrate_tables()
# Создание FastAPI

# Подключаем маршруты
app.include_router(default_router)
app.include_router(homework_router)  # включаем homework_router
app.include_router(lesson_router)
app.include_router(courses_router)
app.include_router(role_router)
app.include_router(attendance_router)
app.include_router(event_router)
