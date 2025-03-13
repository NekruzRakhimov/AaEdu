from fastapi import APIRouter, Depends
from pkg.services import CourseService
from schemas.CourseSchemas import CourseSchema
from pkg.controllers.middlewares import get_current_user
from utils.auth import TokenPayload

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", summary="Получить список курсов")
def get_courses():
    courses = CourseService.get_courses()
    return {"courses": courses}


@router.post("/", summary="Создать новый курс")
def create_course(course_schema: CourseSchema, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id
    return CourseService.create_course(user_id, course_schema)


@router.put("/{course_id}", summary="Обновить курс по ID")
def update_course(course_id: int, course_schema: CourseSchema, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id
    return CourseService.update_course(user_id, course_schema, course_id)


@router.delete("/{course_id}", summary="Удалить курс по ID")
def delete_course(course_id: int, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id
    return CourseService.delete_course(user_id, course_id)
