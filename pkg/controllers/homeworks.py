from fastapi import APIRouter, HTTPException, status, Depends
from starlette.responses import Response
import json

from pkg.services import homework_service as homework_service
from schemas.homeworks import HomeworkSchema, HomeworkUpdateSchema
from db.models import User

router = APIRouter()


def get_current_user():
    user = User(id=2, full_name="Мария Петрова", username="maria", password="hashed_password2", role_id=3)
    return user


def is_mentor(user: User = Depends(get_current_user)):
    if user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only mentors can perform this action")
    return user


@router.get("/homeworks", summary="Get student homeworks", tags=["homeworks"])
def get_homeworks(user: User = Depends(get_current_user)):
    homeworks = homework_service.get_student_homeworks(user)
    return homeworks


@router.post("/homeworks", summary="Add homework", tags=["homeworks"])
def add_homework(homework: HomeworkSchema, user: User = Depends(is_mentor)):
    homework_id = homework_service.add_homework(user, homework.lesson_id, homework.student_id, homework.score)
    return Response(json.dumps({'message': 'Homework successfully added', 'homework_id': homework_id}),
                    status_code=status.HTTP_201_CREATED,
                    media_type='application/json')


@router.put("/homeworks/{homework_id}", summary="Edit homework", tags=["homeworks"])
def edit_homework(homework_id: int, homework_data: HomeworkUpdateSchema, user: User = Depends(is_mentor)):
    updated_homework = homework_service.edit_homework(user, homework_id, homework_data.score)
    if not updated_homework:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Homework not found")
    return {"message": "Homework updated successfully", "homework": updated_homework}


@router.delete("/homeworks/{homework_id}", summary="Delete homework", tags=["homeworks"])
def remove_homework(homework_id: int, user: User = Depends(is_mentor)):
    success = homework_service.remove_homework(user, homework_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Homework not found")
    return Response(json.dumps({'message': 'Homework successfully deleted'}), status_code=status.HTTP_200_OK)
