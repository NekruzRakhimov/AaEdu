import json
from fastapi import APIRouter, status, HTTPException, Depends
from starlette.responses import Response
from pkg.services.homework_service import (
    add_homework, get_student_homeworks, edit_homework, remove_homework
)
from schemas.homeworks import HomeworkCreate, HomeworkResponse
from db.models import User
from decimal import Decimal


router = APIRouter()


# Фейковая функция получения текущего пользователя (здесь можно добавить логику из вашего проекта)
def get_current_user():
    user = User(id=3,
                full_name="Мария Петрова",
                username="maria",
                password="hashed_password2",
                role_id=2)  # 2 - роль ментора
    return user


# Проверка, является ли пользователь ментором
def is_mentor(user: User = Depends(get_current_user)):
    if user.role_id != 2:  # Проверка роли на ментор
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only mentor can perform this action")
    return user


@router.post("/homeworks", summary="Create homework", tags=["homeworks"], response_model=HomeworkResponse)
def create_homework(homework: HomeworkCreate, user: User = Depends(get_current_user)):
    try:
        # Фейковая логика добавления домашки (заменить на реальную логику сервиса)
        homework_data = add_homework(user, homework.lesson_id, homework.student_id, homework.score)
        return Response(
            json.dumps({'message': 'Homework successfully created', 'homework_id': homework_data.id}),
            status_code=status.HTTP_201_CREATED,
            media_type='application/json'
        )
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")


@router.get("/homeworks", summary="Get homeworks", tags=["homeworks"], response_model=list[HomeworkResponse])
def get_homeworks(user: User = Depends(get_current_user)):
    try:
        # Фейковая логика получения домашних заданий
        homeworks = get_student_homeworks(user)
        return homeworks
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")


@router.put("/homeworks/{homework_id}", summary="Update homework", tags=["homeworks"], response_model=HomeworkResponse)
def update_homework(homework_id: int, score: Decimal, user: User = Depends(get_current_user)):
    try:
        # Фейковая логика обновления домашки
        homework = edit_homework(user, homework_id, score)
        if not homework:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Homework not found")
        return homework
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")


@router.delete("/homeworks/{homework_id}", summary="Delete homework", tags=["homeworks"], response_model=HomeworkResponse)
def delete_homework(homework_id: int, user: User = Depends(get_current_user)):
    try:
        # Фейковая логика удаления домашки
        success = remove_homework(user, homework_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Homework not found")
        return Response(
            json.dumps({'message': 'Homework successfully deleted'}),
            status_code=status.HTTP_200_OK,
            media_type='application/json'
        )
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")
