#просмотр уроков, уровень доступа ментор, студент зависимость подписка на курс
from fastapi import Depends

from pkg.controllers.default import router
from pkg.controllers.middlewares import get_current_user
from utils.auth import TokenPayload


@router.get("/lessons", summary="Get all tasks", tags=["tasks"])
def get_all_lessons(payload: TokenPayload = Depends(get_current_user)):
    pass
from fastapi import APIRouter, status, Depends
from starlette.responses import Response, JSONResponse
from pkg.controllers.middlewares import get_current_user
from pkg.services import lesson as lesson_service
from schemas.lesson import LessonSchema

from utils.auth import TokenPayload

router = APIRouter()


# просмотр уроков, уровень доступа ментор, студент зависимость подписка на курс
@router.get("/lessons/{course_id}", summary="Get all lessons", tags=["lessons"])
def get_all_lessons(course_id: int, payload: TokenPayload = Depends(get_current_user)):
    # TODO: check role

    lessons = lesson_service.get_lessons(course_id)
    return lessons


# просмотр урока, уровень доступа ментор, студент зависимость подписка на курс
@router.get("/lesson/{course_id}/{lesson_id}", summary="Get lessons by ID", tags=["lessons"])
def get_lesson_by_id(course_id: int, lesson_id: int, payload: TokenPayload = Depends(get_current_user)):
    # TODO: check role

    lesson = lesson_service.get_lesson_by_id(course_id, lesson_id)
    if lesson is None:
        return JSONResponse({"message": "Lesson not found"}, status_code=status.HTTP_404_NOT_FOUND)
    return lesson


#добавление урока, уровень доступа ментор зависимость подписка на курс
@router.post("/lesson", summary="Get all tasks", tags=["tasks"])
def create_course(payload: TokenPayload = Depends(get_current_user)):
    pass

#изменение урока, уровень доступа ментор зависимость подписка на курс
@router.put("/lesson", summary="Get all tasks", tags=["tasks"])
def create_course(payload: TokenPayload = Depends(get_current_user)):
    pass

#удаление урока, уровень доступа ментор зависимость подписка на курс
@router.delete("/lesson", summary="Get all tasks", tags=["tasks"])
def create_course(payload: TokenPayload = Depends(get_current_user)):
    pass