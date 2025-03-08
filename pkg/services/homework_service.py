from pkg.repositories.homeworks import (
    create_homework, get_homework_by_id, get_homeworks_by_student,
    update_homework, delete_homework, get_course_by_lesson, is_mentor_in_course
)
from fastapi import HTTPException


def is_mentor_of_course(mentor_id, lesson_id):
    course_id = get_course_by_lesson(lesson_id)
    if course_id is None:
        raise HTTPException(status_code=404, detail="Course not found for this lesson.")
    return is_mentor_in_course(mentor_id, course_id)


def add_homework(payload, lesson_id, student_id, score):
    # Проверяем, является ли ментор ментором курса, к которому относится урок
    if not is_mentor_of_course(payload.id, lesson_id):
        raise PermissionError("Only mentors of the course can grade students.")

    homework = create_homework(lesson_id, student_id, score, mentor_id=payload.id)
    return {"id": homework.id}  # Возвращаем только ID


def get_student_homeworks(payload):
    return get_homeworks_by_student(payload.id)


def edit_homework(payload, homework_id, score):
    homework = get_homework_by_id(homework_id)
    if not homework:
        raise HTTPException(status_code=404, detail="Homework not found.")

    if not is_mentor_of_course(payload.id, homework.lesson_id):
        raise PermissionError("Only mentors of the course can edit the homework grade.")

    updated_homework = update_homework(homework_id, score)
    if not updated_homework:
        raise HTTPException(status_code=500, detail="Failed to update homework.")
    return updated_homework


def remove_homework(payload, homework_id):
    homework = get_homework_by_id(homework_id)
    if not homework:
        raise HTTPException(status_code=404, detail="Homework not found.")

    if not is_mentor_of_course(payload.id, homework.lesson_id):
        raise PermissionError("Only mentors of the course can delete the homework.")

    success = delete_homework(homework_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete homework.")
    return {"message": "Homework successfully deleted."}
