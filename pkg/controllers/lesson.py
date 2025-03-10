
from fastapi import APIRouter, status, Depends, HTTPException
from starlette.responses import Response, JSONResponse
from pkg.controllers.middlewares import get_current_user
from pkg.services import lesson as lesson_service
from schemas.lesson import LessonSchema

from utils.auth import TokenPayload

router = APIRouter()


# просмотр уроков, уровень доступа ментор, студент зависимость подписка на курс
@router.get("/lessons/{course_id}", summary="Get all lessons", tags=["lessons"])
def get_all_lessons(course_id: int, payload: TokenPayload = Depends(get_current_user)):
    if payload.role_id not in [1, 2, 3]:
        raise HTTPException(status_code=403, detail="Access denied")

    lessons = lesson_service.get_lessons(course_id)
    return lessons


# просмотр урока, уровень доступа ментор, студент зависимость подписка на курс
@router.get("/lesson/{course_id}/{lesson_id}", summary="Get lessons by ID", tags=["lessons"])
def get_lesson_by_id(course_id: int, lesson_id: int, payload: TokenPayload = Depends(get_current_user)):
    if payload.role_id not in [1, 2, 3]:
        raise HTTPException(status_code=403, detail="Access denied")

    lesson = lesson_service.get_lesson_by_id(course_id, lesson_id)
    if lesson is None:
        return JSONResponse({"message": "Lesson not found"}, status_code=status.HTTP_404_NOT_FOUND)
    return lesson


# добавление урока, уровень доступа ментор зависимость подписка на курс
@router.post("/lesson/{course_id}", summary="Greate new lesson", tags=["lessons"])
def create_lesson(course_id: int, lesson: LessonSchema, payload: TokenPayload = Depends(get_current_user)):
    if payload.role_id not in [2, 3]:
        raise HTTPException(status_code=403, detail="Access denied")

    lesson_service.create_lesson(course_id, lesson)

    return JSONResponse({"message": "Lesson created"}, status_code=status.HTTP_201_CREATED)


# изменение урока, уровень доступа ментор зависимость подписка на курс
@router.put("/lesson/{course_id}/{lesson_id}", summary="Get all tasks", tags=["lessons"])
def update_lesson(course_id: int, lesson_id: int, lesson: LessonSchema, payload: TokenPayload = Depends(get_current_user)):
    if payload.role_id not in [2, 3]:
        raise HTTPException(status_code=403, detail="Access denied")

    lesson = lesson_service.update_lesson(course_id, lesson_id, lesson)
    if lesson is None:
        return JSONResponse({"message": "Lesson not found"}, status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse({"message": "Lesson updated"}, status_code=status.HTTP_200_OK)


# удаление урока, уровень доступа ментор зависимость подписка на курс
@router.delete("/lesson/{course_id}/{lesson_id}", summary="Get all tasks", tags=["lessons"])
def delete_lesson(course_id: int, lesson_id: int, payload: TokenPayload = Depends(get_current_user)):
    if payload.role_id not in [2, 3]:
        raise HTTPException(status_code=403, detail="Access denied")

    lesson = lesson_service.delete_lesson(course_id, lesson_id)
    if lesson is None:
        return JSONResponse({"message": "Lesson not found"}, status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
