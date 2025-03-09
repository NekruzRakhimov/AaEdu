import datetime
from sqlalchemy.orm import Session
from db.postgres import engine
from db.models import Homework, CourseUser, Lesson


def get_course_by_lesson(lesson_id: int):
    with Session(bind=engine) as db:
        lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if not lesson:
            print(f"Lesson with id {lesson_id} not found.")  # Отладка
        else:
            print(f"Lesson {lesson_id} is in course {lesson.course_id}.")  # Отладка
        return lesson.course_id if lesson else None


def is_mentor_of_course(mentor_id: int, lesson_id: int):
    """ Проверяет, является ли пользователь ментором курса, в котором находится данный урок. """
    course_id = get_course_by_lesson(lesson_id)
    if not course_id:
        return False

    with Session(bind=engine) as db:
        mentor_count = db.query(CourseUser).filter(
            CourseUser.user_id == mentor_id,
            CourseUser.course_id == course_id
        ).count()
        return mentor_count > 0


def create_homework(homework: Homework):
    with Session(bind=engine) as db:
        db.add(homework)
        db.commit()
        db.refresh(homework)
        return homework


def get_homework_by_id(homework_id: int):
    with Session(bind=engine) as db:
        return db.query(Homework).filter(Homework.id == homework_id).first()


def get_homeworks_by_student(student_id: int):
    with Session(bind=engine) as db:
        return db.query(Homework).filter(Homework.student_id == student_id).all()


def update_homework(homework_id: int, score: float):
    with Session(bind=engine) as db:
        homework = db.query(Homework).filter(Homework.id == homework_id).first()
        if homework:
            homework.score = score
            homework.updated_at = datetime.datetime.now()
            db.commit()
            db.refresh(homework)
            return homework
        return None


def delete_homework(homework_id: int):
    with Session(bind=engine) as db:
        homework = db.query(Homework).filter(Homework.id == homework_id).first()
        if homework:
            db.delete(homework)
            db.commit()
            return True
        return False
