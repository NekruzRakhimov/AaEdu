# просмотр всех курсов, уровень доступа все
from fastapi import Depends

from pkg.controllers.default import router
from pkg.controllers.middlewares import get_current_user
from utils.auth import TokenPayload


@router.get("/courses", summary="Get all tasks", tags=["tasks"])
def get_all_courses(payload: TokenPayload = Depends(get_current_user)):
    pass

# добавление курса, уровень доступа админ
@router.post("/course", summary="Get all tasks", tags=["tasks"])
def create_course(payload: TokenPayload = Depends(get_current_user)):
    pass

# измениние курса, уровень доступа админ
@router.put("/course", summary="Get all tasks", tags=["tasks"])
def create_course(payload: TokenPayload = Depends(get_current_user)):
    pass

# удаление курса, уровень доступа админ
@router.delete("/course", summary="Get all tasks", tags=["tasks"])
def create_course(payload: TokenPayload = Depends(get_current_user)):
    pass
