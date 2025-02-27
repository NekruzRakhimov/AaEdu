#просмотр уроков, уровень доступа ментор, студент зависимость подписка на курс
@router.get("/lessons", summary="Get all tasks", tags=["tasks"])
def get_all_lessons(payload: TokenPayload = Depends(get_current_user)):
    pass

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