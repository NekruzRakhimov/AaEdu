import uvicorn
from fastapi import FastAPI

from configs.config import settings
from pkg.controllers.homeworks import router as homeworks_router
from db.models import migrate_tables
from pkg.controllers.default import router as default_router
from pkg.controllers.lesson import router as lesson_router
from pkg.controllers.CourseController import router as courses_router
from pkg.controllers.auth import router as auth_router
from pkg.controllers.attendances import router as attendance_router
from pkg.controllers.role import router as role_router
from pkg.controllers.event import router as event_router
from pkg.controllers.course_members import router as course_members_router
from pkg.controllers.lesson_material import router as material_router


if __name__ == "__main__":
    # Создание таблиц
    migrate_tables()

    # Создание роутера
    app = FastAPI()

    # Подключаем маршруты
    app.include_router(auth_router)
    app.include_router(homeworks_router)
    app.include_router(default_router)
    app.include_router(lesson_router)
    app.include_router(courses_router)
    app.include_router(role_router)
    app.include_router(attendance_router)
    app.include_router(event_router)
    app.include_router(material_router)
    uvicorn.run(app, port=settings.port, host=settings.host)
