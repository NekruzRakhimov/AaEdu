from fastapi import HTTPException
from db.models import Homework, User
from pkg.repositories import homeworks as homework_repository
from schemas.homeworks import HomeworkSchema


def get_student_homeworks(user: User):
    return homework_repository.get_homeworks_by_student(user.id)


def add_homework(user: User, lesson_id: int, student_id: int, score: float):
    if not homework_repository.is_mentor_of_course(user.id, lesson_id):
        raise HTTPException(status_code=403, detail="Only mentors of the course can grade students")

    homework = Homework(lesson_id=lesson_id, student_id=student_id, score=score, mentor_id=user.id)
    return homework_repository.create_homework(homework)


def edit_homework(user: User, homework_id: int, score: float):
    homework = homework_repository.get_homework_by_id(homework_id)
    if not homework:
        raise HTTPException(status_code=404, detail="Homework not found")

    if not homework_repository.is_mentor_of_course(user.id, homework.lesson_id):
        raise HTTPException(status_code=403, detail="Only mentors of the course can edit the homework grade")

    return homework_repository.update_homework(homework_id, score)


def remove_homework(user: User, homework_id: int):
    homework = homework_repository.get_homework_by_id(homework_id)
    if not homework:
        raise HTTPException(status_code=404, detail="Homework not found")

    if not homework_repository.is_mentor_of_course(user.id, homework.lesson_id):
        raise HTTPException(status_code=403, detail="Only mentors of the course can delete the homework")

    return homework_repository.delete_homework(homework_id)
