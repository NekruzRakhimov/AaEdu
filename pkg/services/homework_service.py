from db.models import Homework
from pkg.repositories.homeworks import (
    create_homework, get_homework_by_id, get_homeworks_by_student,
    update_homework, delete_homework, get_course_by_lesson, is_mentor_in_course
)


def is_mentor_of_course(mentor_id, lesson_id):
    course_id = get_course_by_lesson(lesson_id)

    return is_mentor_in_course(mentor_id, course_id)


def add_homework(payload, lesson_id, student_id, score):
    # Проверяем, является ли ментор ментором курса, к которому относится урок
    if not is_mentor_of_course(payload.id, lesson_id):
        raise PermissionError("Only mentors of the course can grade students.")

    return create_homework(lesson_id, student_id, score, mentor_id=payload.id)


def get_student_homeworks(payload):
    return get_homeworks_by_student(payload.id)


def edit_homework(payload, homework_id, score):
    homework = get_homework_by_id(homework_id)
    if not homework:
        return None

    if not is_mentor_of_course(payload.id, homework.lesson_id):
        raise PermissionError("Only mentors of the course can edit the homework grade.")

    return update_homework(homework_id, score)


def remove_homework(payload, homework_id):
    homework = get_homework_by_id(homework_id)
    if not homework:
        return False

    if not is_mentor_of_course(payload.id, homework.lesson_id):
        raise PermissionError("Only mentors of the course can delete the homework.")

    return delete_homework(homework_id)
