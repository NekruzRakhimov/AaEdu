import datetime

from sqlalchemy.orm import Session
from db.postgres import engine
from db.models import Comment
from schemas.comments import CommentSchema
from logger.logger import logger


def get_comments(lesson_id: int):
    with Session(bind=engine) as db:
        db_comments = db.query(Comment).filter(
            Comment.lesson_id == lesson_id,
        ).all()

    return db_comments

def get_comment_by_id(lesson_id: int, comment_id: int):
    with Session(bind=engine) as db:
        db_comment = db.query(Comment).filter(
            Comment.lesson_id == lesson_id,
            Comment.id == comment_id,
        ).first()

    if db_comment is None:
        logger.error(f"Comment with id {comment_id} not found")

    return db_comment

def create_comment(comment: Comment):
    with Session(bind=engine) as db:
        db.add(comment)
        db.commit()
        db.refresh(comment)

        return comment.id

def update_comment(lesson_id: int, comment_id: int, comment: CommentSchema):
    with Session(bind=engine) as db:
        db_comment = db.query(Comment).filter(
            Comment.id == comment_id,
            Comment.lesson_id == lesson_id,
        ).first()

        if not db_comment:
            logger.error(f"Comment with id {comment_id} not found")
            return None

        db_comment.text = comment.text
        db.commit()

        return db_comment

def delete_comment(lesson_id: int, comment_id: int):
    with Session(bind=engine) as db:
        db_comment = db.query(Comment).filter(
            Comment.id == comment_id,
                     Comment.lesson_id == lesson_id,
        ).first()

        if not db_comment:
            logger.error(f"Comment with id {comment_id} not found")
            return None

        db_comment.deleted_at = datetime.datetime.now()
        db.commit()

        return db_comment
