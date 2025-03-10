from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.postgres import engine
from pkg.services import comments as comment_service
from schemas.comments import CommentSchema

router = APIRouter()


@router.get("/lessons/comments", summary= "Read comments", tags=["comments"])
def get_comments(lesson_id):
    comments = comment_service.get_comments(lesson_id)
    return comments

@router.post("/lessons/{lesson_id}/comments", summary= "Create comment", tags=["comments"])
def create_comment(lesson_id: int, comment: CommentSchema):
    return comment_service.create_comment(lesson_id, comment)

@router.put("/lessons/{lesson_id}/comments/{comment_id}", summary= "Update comment", tags=["comments"])
def update_comment(lesson_id: int, comment_id: int, comment: CommentSchema):
    updated_comment = comment_service.update_comment(lesson_id, comment_id, comment)
    if not updated_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return updated_comment

@router.delete("/lessons/{lesson_id}/comments/{comment_id}", summary="Delete comments", tags=["comments"])
def delete_comment(lesson_id: int, comment_id: int):
    deleted_comment = comment_service.delete_comment(lesson_id, comment_id)
    if not deleted_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return deleted_comment
