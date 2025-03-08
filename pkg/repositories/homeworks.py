from sqlalchemy.orm import Session
from db.models import Homework, CourseUser, Lesson
from decimal import Decimal, InvalidOperation
from db.postgres import engine


def get_course_by_lesson(lesson_id):
    with Session(bind=engine) as db:
        lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if not lesson:
            return None
        return lesson.course_id


def is_mentor_in_course(mentor_id, course_id):
    with Session(bind=engine) as db:
        return db.query(CourseUser).filter(
            CourseUser.user_id == mentor_id,
            CourseUser.role_in_course == 'mentor',
            CourseUser.course_id == course_id
        ).count() > 0


def create_homework(lesson_id, student_id, score, mentor_id):
    try:
        score = Decimal(score)
    except InvalidOperation:
        raise ValueError("Invalid score value. It must be a valid decimal.")

    homework = Homework(lesson_id=lesson_id, student_id=student_id, score=score, mentor_id=mentor_id)
    with Session() as db:
        db.add(homework)
        db.commit()
        db.refresh(homework)
    return homework


def get_homework_by_id(homework_id):
    with Session(bind=engine) as db:
        return db.query(Homework).filter(Homework.id == homework_id).first()


def get_homeworks_by_student(student_id):
    with Session(bind=engine) as db:
        return db.query(Homework).filter(Homework.student_id == student_id).all()


def update_homework(homework_id, score):
    try:
        score = Decimal(score)
    except InvalidOperation:
        raise ValueError("Invalid score value. It must be a valid decimal.")

    with Session(bind=engine) as db:
        homework = db.query(Homework).filter(Homework.id == homework_id).first()
        if homework:
            homework.score = score
            db.commit()
            db.refresh(homework)
            return homework
        return None


def delete_homework(homework_id):
    with Session(bind=engine) as db:
        homework = db.query(Homework).filter(Homework.id == homework_id).first()
        if homework:
            db.delete(homework)
            db.commit()
            return True
        return False
