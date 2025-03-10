from fastapi import APIRouter, HTTPException, Depends
from typing import List

from decimal import Decimal

from pkg.services.homework_service import (
    add_homework, get_student_homeworks, edit_homework, remove_homework
)
from schemas.homeworks import HomeworkCreate, HomeworkResponse
from utils.auth import TokenPayload
from pkg.controllers.middlewares import get_current_user

router = APIRouter()


@router.post("/", summary="create homework", tags=["homeworks"], response_model=HomeworkResponse)
def create_homework(homework: HomeworkCreate, payload: TokenPayload = Depends(get_current_user)):
    try:
        return add_homework(payload, homework.lesson_id, homework.student_id, homework.score)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get("/", summary="get homeworks", tags=["homeworks"], response_model=List[HomeworkResponse])
def get_homeworks(payload: TokenPayload = Depends(get_current_user)):
    return get_student_homeworks(payload)


@router.put("/{homework_id}", summary="update homework", tags=["homeworks"], response_model=HomeworkResponse)
def update_homework(homework_id: int, score: Decimal, payload: TokenPayload = Depends(get_current_user)):
    try:
        homework = edit_homework(payload, homework_id, score)
        if not homework:
            raise HTTPException(status_code=404, detail="Homework not found")
        return homework
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/{homework_id}", summary="delete homework", tags=["homeworks"], response_model=HomeworkResponse)
def delete_homework(homework_id: int, payload: TokenPayload = Depends(get_current_user)):
    try:
        success = remove_homework(payload, homework_id)
        if not success:
            raise HTTPException(status_code=404, detail="Homework not found")
        return {"message": "Homework deleted successfully"}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
