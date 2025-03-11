import datetime

from sqlalchemy import desc
from sqlalchemy.orm import Session
from db.postgres import engine
from db.models import Comment
from schemas.comments import CommentSchema
from logger.logger import logger



def create_comment(comment: Comment):
    with Session(bind=engine) as db:
        comment_db = Comment(
            lesson_id=comment.lesson_id,
            user_id=comment.user_id,
            content=comment.content,
        )
        db.add(comment_db)
        db.commit()
        db.refresh(comment_db)
        return comment_db.id

def get_comments():
    with Session(bind=engine) as db:
        db_comments = db.query(Comment).filter(
            Comment.deleted_at == None).order_by(desc(Comment.created_at)).all()

    return db_comments

def get_comment_by_id(user_id: int, lesson_id: int, comment_id: int):
    with Session(bind=engine) as db:
        db_comment = db.query(Comment).filter(
            Comment.lesson_id == lesson_id,
            Comment.id == comment_id,
            Comment.user_id == user_id,
            Comment.deleted_at == None,  # Only consider non-deleted comments
        ).first()

    if db_comment is None:
        logger.error(f"Comment with id {comment_id} not found")

    return db_comment



def update_comment(user_id: int, lesson_id: int, comment_id: int, comment: CommentSchema):
    with Session(bind=engine) as db:
        db_comment = get_comment_by_id(user_id, lesson_id, comment_id)

        if not db_comment:
            logger.error(f"Comment with id {comment_id} not found")
            return None

        db_comment.content = comment.content
        db_comment.update_at = datetime.datetime.now()
        db.commit()

        return db_comment

def soft_delete_comment(user_id: int, lesson_id: int, comment_id: int):
    with Session(bind=engine) as db:
        db_comment = get_comment_by_id(user_id, lesson_id, comment_id)
        if not db_comment:
            logger.error(f"Comment with id {comment_id} not found")
            return None

        db_comment.deleted_at = datetime.datetime.now()
        db.commit()

        return db_comment

def hard_delete_comment(user_id: int, lesson_id: int, comment_id: int):
    with Session(bind=engine) as db:
        db_comment = get_comment_by_id(user_id, lesson_id, comment_id)

        if not db_comment:
            logger.error(f"Comment with id {comment_id} not found")
            return None

        db.delete(db_comment)
        db.commit()

        return db_comment