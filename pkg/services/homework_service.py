from db.models import Homework
from typing import List, Optional
from decimal import Decimal
from pkg.repositories.homeworks import (
    create_homework, get_homework_by_id, get_homeworks_by_student,
    update_homework, delete_homework, get_student_courses, is_mentor_in_courses
)
from utils.auth import TokenPayload


def is_mentor_of_student(mentor_id: int, student_id: int) -> bool:
    student_courses = get_student_courses(student_id)
    return is_mentor_in_courses(mentor_id, student_courses)


def add_homework(payload: TokenPayload, lesson_id: int, student_id: int, score: Decimal) -> Optional[Homework]:
    if not is_mentor_of_student(payload.id, student_id):
        raise PermissionError("Только менторы курса могут выставлять оценки этому студенту")

    return create_homework(lesson_id, student_id, score, mentor_id=payload.id)


def get_student_homeworks(payload: TokenPayload) -> List[Homework]:
    return get_homeworks_by_student(payload.id)


def edit_homework(payload: TokenPayload, homework_id: int, score: Decimal) -> Optional[Homework]:
    homework = get_homework_by_id(homework_id)
    if not homework:
        return None

    if not is_mentor_of_student(payload.id, homework.student_id):
        raise PermissionError("Только менторы курса могут редактировать эту оценку")

    return update_homework(homework_id, score)


def remove_homework(payload: TokenPayload, homework_id: int) -> bool:
    homework = get_homework_by_id(homework_id)
    if not homework:
        return False

    if not is_mentor_of_student(payload.id, homework.student_id):
        raise PermissionError("Только менторы курса могут удалять эту оценку")

    return delete_homework(homework_id)
