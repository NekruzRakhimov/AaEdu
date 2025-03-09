from fastapi import APIRouter, status, Depends
from starlette.responses import Response, JSONResponse
from pkg.controllers.middlewares import get_current_user
from pkg.services import course_user as course_user_service
from pkg.schemas.course_user import CourseUserCreate
from utils.auth import TokenPayload

router = APIRouter()


# Получение списка пользователей курса (уровень доступа: ментор, админ)
@router.get("/course_user/{course_id}", summary="Get all course users", tags=["course_user"])
def get_course_users(course_id: int, payload: TokenPayload = Depends(get_current_user)):
    # TODO: check role

    users = course_user_service.get_course_users(course_id)
    return users


# Добавление пользователя в курс (уровень доступа: админ)
@router.post("/course_user/{course_id}", summary="Add user to course", tags=["course_user"])
def add_user_to_course(course_id: int, user: CourseUserCreate, payload: TokenPayload = Depends(get_current_user)):
    # TODO: check role

    course_user_service.add_user_to_course(course_id, user)

    return JSONResponse({"message": "User added to course"}, status_code=status.HTTP_201_CREATED)


# Удаление пользователя из курса (уровень доступа: админ)
@router.delete("/course_user/{course_id}/{user_id}", summary="Remove user from course", tags=["course_user"])
def remove_user_from_course(course_id: int, user_id: int, payload: TokenPayload = Depends(get_current_user)):
    # TODO: check role

    deleted_user = course_user_service.remove_user_from_course(course_id, user_id)
    if deleted_user is None:
        return JSONResponse({"message": "User not found in course"}, status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
