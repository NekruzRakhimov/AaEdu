from fastapi import APIRouter, HTTPException, status, Depends
from starlette.responses import Response
import json

from pkg.controllers.middlewares import get_current_user
from pkg.services import homework_service as homework_service
from schemas.homeworks import HomeworkSchema, HomeworkUpdateSchema
from utils.auth import TokenPayload


router = APIRouter()


def is_mentor(payload: TokenPayload = Depends(get_current_user)):
    if payload.role != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only mentors can perform this action")
    return payload


@router.get("/homeworks", summary="Get student homeworks", tags=["homeworks"])
def get_homeworks(payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id
    return {"homeworks": homework_service.get_student_homeworks(user_id)}


@router.post("/homeworks", summary="Add homework", tags=["homeworks"])
def add_homework(homework: HomeworkSchema, payload: TokenPayload = Depends(is_mentor)):
    user_id = payload.id
    homework = homework_service.add_homework(user_id, homework.lesson_id, homework.student_id, homework.score)
    return Response(json.dumps({'message': 'Homework successfully added', 'homework_id': homework.id}),
                    status_code=status.HTTP_201_CREATED,
                    media_type='application/json')


@router.put("/homeworks/{homework_id}", summary="Edit homework", tags=["homeworks"])
def edit_homework(homework_id: int, homework_data: HomeworkUpdateSchema, payload: TokenPayload = Depends(is_mentor)):
    user_id = payload.id
    updated_homework = homework_service.edit_homework(user_id, homework_id, homework_data.score)
    if not updated_homework:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Homework not found")
    return {"message": "Homework updated successfully", "homework": updated_homework}


@router.delete("/homeworks/{homework_id}", summary="Delete homework", tags=["homeworks"])
def remove_homework(homework_id: int, payload: TokenPayload = Depends(is_mentor)):
    user_id = payload.id
    success = homework_service.remove_homework(user_id, homework_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Homework not found")
    return Response(json.dumps({'message': 'Homework successfully deleted'}), status_code=status.HTTP_200_OK)
