from fastapi import HTTPException
from db.models import Homework, User
from pkg.repositories import homeworks as homework_repository
from schemas.homeworks import HomeworkSchema


def get_student_homeworks(user: User):
    return homework_repository.get_homeworks_by_student(user.id)


def add_homework(user: User, homework: HomeworkSchema):
    if not homework_repository.is_mentor_of_course(user.id, homework.lesson_id):
        raise HTTPException(status_code=403, detail="Only mentors of the course can grade students")

    h = Homework()
    h.course_id = homework.course_id
    h.lesson_id = homework.lesson_id
    h.student_id = homework.student_id
    h.mentor_id = homework.mentor_id
    h.homework = homework.homework
    h.score = homework.score
    h.deleted_at = None

    return homework_repository.create_homework(h)


def edit_homework(user: User, homework_id: int, score: float):
    homework = homework_repository.get_homework_by_id(homework_id)
    if not homework:
        raise HTTPException(status_code=404, detail="Homework not found")
    course_id = homework_repository.get_course_by_lesson(homework.lesson_id)
    if not course_id:
        raise HTTPException(status_code=404, detail="Course not found for this lesson")
    if not homework_repository.is_mentor_of_course(user.id, course_id):
        raise HTTPException(status_code=403, detail="Only mentors of the course can edit the homework grade")

    return homework_repository.update_homework(homework_id, score)


def remove_homework(user: User, homework_id: int):
    homework = homework_repository.get_homework_by_id(homework_id)
    if not homework:
        raise HTTPException(status_code=404, detail="Homework not found")

    course_id = homework_repository.get_course_by_lesson(homework.lesson_id)
    if not course_id:
        raise HTTPException(status_code=404, detail="Course not found for this lesson")

    if not homework_repository.is_mentor_of_course(user.id, course_id):
        raise HTTPException(status_code=403, detail="Only mentors of the course can delete the homework")

    return homework_repository.delete_homework(homework_id)



def soft_delete_homework(homework_id: int):
    homework = homework_repository.get_homework_by_id(homework_id)
    if not homework:
        raise HTTPException(status_code=404, detail="Homework not found")
    return homework_repository.soft_delete_homework(homework_id)