# просмотр моих курсов
from fastapi import Depends

from pkg.controllers.default import router
from pkg.controllers.middlewares import get_current_user
from utils.auth import TokenPayload


@router.get("/my_courses", summary="Get all tasks", tags=["tasks"])
def get_my_courses(payload: TokenPayload = Depends(get_current_user)):
    pass

#регистрация на курс
@router.post("/course/{course_id}", summary="Get all tasks", tags=["tasks"])
def registory_for_course(payload: TokenPayload = Depends(get_current_user)):
    pass

#отписаться от курса
@router.delete("/course/{course_id}", summary="Get all tasks", tags=["tasks"])
def unfollow_from_course(payload: TokenPayload = Depends(get_current_user)):
    pass

