from db.models import Lesson
from pkg.repositories import lesson as lesson_repository
from schemas.lesson import LessonSchema


def get_lessons(course_id: int):
    lessons = lesson_repository.get_lessons(course_id)
    return lessons


def get_lesson_by_id(course_id: int, lesson_id: int):
    lesson = lesson_repository.get_lesson_by_id(course_id, lesson_id)
    return lesson


def create_lesson(course_id: int, lesson: LessonSchema):
    # TODO: check if course exists

    l = Lesson()
    l.title = lesson.title
    l.description = lesson.description
    l.content = lesson.content
    l.course_id = course_id

    return lesson_repository.create_lesson(l)


def update_lesson(course_id: int, lesson_id: int, lesson: LessonSchema):
    # TODO: check if course exists

    return lesson_repository.update_lesson(course_id, lesson_id, lesson)


def delete_lesson(course_id: int, lesson_id: int):
    return lesson_repository.delete_lesson(course_id, lesson_id)
