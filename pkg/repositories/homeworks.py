from sqlalchemy.orm import Session
from db.models import Homework, CourseUser
from typing import List, Optional
from decimal import Decimal
from db.postgres import engine


def get_student_courses(student_id: int) -> List[int]:
    """Получает список ID курсов, в которых состоит студент."""
    with Session(bind=engine) as db:
        return [
            course.course_id for course in db.query(CourseUser.course_id)
            .filter(CourseUser.user_id == student_id)
            .all()
        ]


def is_mentor_in_courses(mentor_id: int, course_id: List[int]) -> bool:
    """Проверяет, является ли пользователь ментором хотя бы в одном из курсов."""
    with Session(bind=engine) as db:
        return db.query(CourseUser).filter(
            CourseUser.user_id == mentor_id,
            CourseUser.role_in_course == 'mentor',
            CourseUser.course_id.in_(course_id)
        ).first() is not None


def create_homework(lesson_id: int, student_id: int, score: Decimal, mentor_id: int) -> Homework:
    with Session() as db:
        homework = Homework(lesson_id=lesson_id, student_id=student_id, score=score, mentor_id=mentor_id)
        db.add(homework)
        db.commit()
        db.refresh(homework)
        return homework


def get_homework_by_id(homework_id: int) -> Optional[Homework]:
    with Session(bind=engine) as db:
        return db.query(Homework).filter(Homework.id == homework_id).first()


def get_homeworks_by_student(student_id: int) -> List[Homework]:
    with Session(bind=engine) as db:
        return db.query(Homework).filter(Homework.student_id == student_id).all()


def update_homework(homework_id: int, score: Decimal) -> Optional[Homework]:
    with Session(bind=engine) as db:
        homework = db.query(Homework).filter(Homework.id == homework_id).first()
        if homework:
            homework.score = score
            db.commit()
            db.refresh(homework)
        return homework


def delete_homework(homework_id: int) -> bool:
    with Session(bind=engine) as db:
        homework = db.query(Homework).filter(Homework.id == homework_id).first()
        if homework:
            db.delete(homework)
            db.commit()
            return True
        return False
