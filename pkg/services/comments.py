from db.models import Comment
from pkg.repositories import comments as comment_repository
from schemas.comments import CommentSchema

def get_comments():
    return comment_repository.get_comments()

def create_comment(lesson_id: int, comment: CommentSchema):
    # TODO: check if lesson exists

    c = Comment()
    c.content = comment.content
    c.user_id = comment.user_id
    c.lesson_id = lesson_id

    return comment_repository.create_comment(c)

def update_comment(user_id: int, lesson_id: int, comment_id: int, comment: CommentSchema):
    # TODO: check if lesson exists
    service_comment = comment_repository.get_comment_by_id(user_id, lesson_id, comment_id)
    if not service_comment:
        return None

    service_comment.content = comment.content

    return comment_repository.update_comment(user_id, lesson_id, comment_id, comment)

def soft_delete_comment(lesson_id: int, comment_id: int, user_id: int):
    return comment_repository.soft_delete_comment(lesson_id, comment_id, user_id)

def hard_delete_comment(lesson_id: int, comment_id: int, user_id: int):
    return comment_repository.hard_delete_comment(lesson_id, comment_id, user_id)
