
from fastapi import APIRouter, HTTPException, status, Depends
from starlette.responses import Response, JSONResponse
from pkg.controllers.middlewares import get_current_user
from pkg.services import lesson as lesson_service
from schemas.lesson import LessonSchema

from utils.auth import TokenPayload

router = APIRouter()


# просмотр уроков, уровень доступа ментор, студент зависимость подписка на курс
@router.get("/lessons/{course_id}", summary="Get all lessons", tags=["lessons"])
def get_all_lessons(course_id: int, payload: TokenPayload = Depends(get_current_user)):
    if not lesson_service.is_admin_or_metnor(payload.id) and not lesson_service.lesson_repository.is_user_has_access_to_lesson(payload.id, course_id):
        raise HTTPException(
            status_code=403, detail="User does not have access to this course and it's lessons")

    return lesson_service.get_lessons(course_id)


# просмотр урока, уровень доступа ментор, студент зависимость подписка на курс
@router.get("/lesson/{course_id}/{lesson_id}", summary="Get lessons by ID", tags=["lessons"])
def get_lesson_by_id(course_id: int, lesson_id: int, payload: TokenPayload = Depends(get_current_user)):
    if not lesson_service.is_admin_or_metnor(payload.id) and not lesson_service.lesson_repository.is_user_has_access_to_lesson(payload.id, course_id):
        raise HTTPException(
            status_code=403, detail="User does not have access to this course and it's lessons")

    lesson = lesson_service.get_lesson_by_id(course_id, lesson_id)
    if lesson is None:
        return JSONResponse({"message": "Lesson not found"}, status_code=status.HTTP_404_NOT_FOUND)
    return lesson


# добавление урока, уровень доступа ментор зависимость подписка на курс
@router.post("/lesson/{course_id}", summary="Greate new lesson", tags=["lessons"])
def create_lesson(course_id: int, lesson: LessonSchema, payload: TokenPayload = Depends(get_current_user)):
    if not lesson_service.is_admin_or_metnor(payload.id):
        raise HTTPException(
            status_code=403, detail="User does not have access to create lesson")

    if not lesson_service.is_course_exists(course_id):
        return JSONResponse({"message": "Course not found"}, status_code=status.HTTP_404_NOT_FOUND)

    lesson_service.create_lesson(course_id, lesson)

    return JSONResponse({"message": "Lesson created"}, status_code=status.HTTP_201_CREATED)


# изменение урока, уровень доступа ментор зависимость подписка на курс
@router.put("/lesson/{course_id}/{lesson_id}", summary="Get all tasks", tags=["lessons"])
def update_lesson(course_id: int, lesson_id: int, lesson: LessonSchema, payload: TokenPayload = Depends(get_current_user)):
    if not lesson_service.is_admin_or_metnor(payload.id):
        raise HTTPException(
            status_code=403, detail="User does not have access to update lesson")

    if not lesson_service.is_course_exists(course_id):
        return JSONResponse({"message": "Course not found"}, status_code=status.HTTP_404_NOT_FOUND)

    lesson = lesson_service.update_lesson(course_id, lesson_id, lesson)
    if lesson is None:
        return JSONResponse({"message": "Lesson not found"}, status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse({"message": "Lesson updated"}, status_code=status.HTTP_200_OK)


# удаление урока, уровень доступа ментор зависимость подписка на курс
@router.delete("/lesson/{course_id}/{lesson_id}", summary="Get all tasks", tags=["lessons"])
def delete_lesson(course_id: int, lesson_id: int, payload: TokenPayload = Depends(get_current_user)):
    if not lesson_service.is_admin_or_metnor(payload.id):
        raise HTTPException(
            status_code=403, detail="User does not have access to delete lesson")

    lesson = lesson_service.delete_lesson(course_id, lesson_id)
    if lesson is None:
        return JSONResponse({"message": "Lesson not found"}, status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
