from db.models import Comment
from pkg.repositories import comments as comment_repository
from schemas.comments import CommentSchema

def get_comments(lesson_id):
    return comment_repository.get_comments(lesson_id)


def create_comment(lesson_id: int, comment: CommentSchema):
    # TODO: check if lesson exists

    c = Comment()
    c.text = comment.text
    c.user_id = comment.user_id
    c.lesson_id = lesson_id

    return comment_repository.create_comment(c)

def update_comment(lesson_id: int, comment_id: int, comment: CommentSchema):
    # TODO: check if lesson exists

    return comment_repository.update_comment(lesson_id, comment_id, comment)

def delete_comment(lesson_id: int, comment_id: int):
    return comment_repository.delete_comment(lesson_id, comment_id)
