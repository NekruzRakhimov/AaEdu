import datetime

from sqlalchemy.orm import Session
from db.postgres import engine
from db.models import Lesson
from schemas.lesson import LessonSchema
from logger.logger import logger


def get_lessons(course_id: int):
    with Session(bind=engine) as db:
        db_lessons = db.query(Lesson).filter(
            Lesson.course_id == course_id,
            Lesson.deleted_at == None
        ).all()

    return db_lessons


def get_lesson_by_id(course_id: int, lesson_id: int):
    with Session(bind=engine) as db:
        db_lesson = db.query(Lesson).filter(
            Lesson.course_id == course_id,
            Lesson.id == lesson_id,
            Lesson.deleted_at == None
        ).first()

    if db_lesson is None:
        logger.error(f"Lesson with id {lesson_id} not found")

    return db_lesson


def create_lesson(lesson: Lesson):
    with Session(bind=engine) as db:
        db.add(lesson)
        db.commit()
        db.refresh(lesson)

        return lesson.id


def update_lesson(course_id: int, lesson_id: int, lesson: LessonSchema):
    with Session(bind=engine) as db:
        db_lesson = db.query(Lesson).filter(
            Lesson.id == lesson_id,
            Lesson.course_id == course_id,
        ).first()

        if not db_lesson:
            logger.error(f"Lesson with id {lesson_id} not found")
            return None

        db_lesson.title = lesson.title
        db_lesson.description = lesson.description
        db_lesson.content = lesson.content

        db.commit()

        return db_lesson


def delete_lesson(course_id: int, lesson_id: int):
    with Session(bind=engine) as db:
        db_lesson = db.query(Lesson).filter(
            Lesson.id == lesson_id,
            Lesson.course_id == course_id,
        ).first()

        if not db_lesson:
            logger.error(f"Lesson with id {lesson_id} not found")
            return None

        db_lesson.deleted_at = datetime.datetime.now()

        db.commit()

        return db_lesson
