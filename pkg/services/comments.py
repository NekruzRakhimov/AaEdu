
import logging

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

import datetime
from http.client import HTTPException

from db.models import Comment
from pkg.repositories import comments as comment_repository
from pkg.repositories.lesson import get_lesson_by_id
from schemas.comments import CommentSchema

def get_comments(lesson_id: int):
    return comment_repository.get_comments(lesson_id)

def create_comment(course_id: int, lesson_id: int, comment: CommentSchema):
    lesson = get_lesson_by_id(course_id, lesson_id)
    if not lesson:
        return None

    c = Comment()
    c.content = comment.content
    c.user_id = comment.user_id
    c.lesson_id = lesson_id

    created_comment = comment_repository.create_comment(c)

    return created_comment

def update_comment(user_id: int, lesson_id: int, comment_id: int, comment: CommentSchema):
    service_comment = comment_repository.get_comment_by_id(user_id, lesson_id, comment_id)
    if not service_comment:
        return None

    service_comment.content = comment.content
    service_comment.updated_at = datetime.datetime.now()

    return comment_repository.update_comment(user_id, lesson_id, comment_id, comment)

def soft_delete_comment(user_id: int, lesson_id: int, comment_id: int):
    return comment_repository.soft_delete_comment(user_id, lesson_id, comment_id)

def hard_delete_comment(user_id: int, lesson_id: int, comment_id: int):
    return comment_repository.hard_delete_comment(user_id, lesson_id, comment_id)


def get_comment_by_id(comment_id: int, user_id: int):
    return comment_repository.get_comment_by_id(comment_id, user_id)