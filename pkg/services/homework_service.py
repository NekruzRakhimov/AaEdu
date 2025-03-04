from pkg.repositories.homeworks import create_homework,get_homework_by_id,get_homeworks_by_student,update_homework,delete_homework

from db.models import CourseUser, Homework
from typing import List, Optional
from pkg.controllers.middlewares import get_current_user
from utils.auth import TokenPayload


def add_homework(payload: TokenPayload, lesson_id: int, student_id: int, score: float) -> Optional[Homework]:
    mentor_id = payload.id

    mentor = CourseUser.query.filter(
        CourseUser.user_id == mentor_id,
        CourseUser.role_in_course == 'mentor'
    ).first()

    if not mentor:
        raise PermissionError("Только менторы могут выставлять оценки")

    return create_homework(lesson_id, student_id, score)


def get_student_homeworks(payload: TokenPayload) -> List[Homework]:
    student_id = payload.id
    return get_homeworks_by_student(student_id)


def edit_homework(payload: TokenPayload, homework_id: int, score: float) -> Optional[Homework]:
    mentor_id = payload.id

    mentor = CourseUser.query.filter(
        CourseUser.user_id == mentor_id,
        CourseUser.role_in_course == 'mentor'
    ).first()

    if not mentor:
        raise PermissionError("Только менторы могут редактировать оценки")

    return update_homework(homework_id, score)


def remove_homework(payload: TokenPayload, homework_id: int) -> bool:
    mentor_id = payload.id

    mentor = CourseUser.query.filter(
        CourseUser.user_id == mentor_id,
        CourseUser.role_in_course == 'mentor'
    ).first()

    if not mentor:
        raise PermissionError("Только менторы могут удалять оценки")

    return delete_homework(homework_id)