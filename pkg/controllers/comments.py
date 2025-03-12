import json
from fastapi import APIRouter, Depends
from starlette.responses import Response
from fastapi import HTTPException

from pkg.controllers.middlewares import get_current_user
from pkg.services import comments as comment_service
from schemas.comments import CommentSchema
from utils.auth import TokenPayload

router = APIRouter()

@router.get("/lessons{lesson}/comments", summary= "Read comments", tags=["Comments"])
def get_comments():
    comments = comment_service.get_comments()
    return comments


@router.post("/lessons/{lesson_id}/comments", summary= "Create comment", tags=["Comments"])
def create_comment(course_id: int, lesson_id: int, comment: CommentSchema, payload: TokenPayload = Depends(get_current_user)):
    if payload.role_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return comment_service.create_comment(course_id, lesson_id, comment)

@router.put("/lessons/{lesson_id}/comments/{comment_id}", summary= "Update comment", tags=["Comments"])
def update_comment(lesson_id: int, comment_id: int, user_id: int, comment: CommentSchema, payload: TokenPayload = Depends(get_current_user)):

    existing_comment = comment_service.get_comment_by_id(comment_id, user_id)
    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if payload.user_id != existing_comment.user_id and payload.role_id != 3:
        raise HTTPException(status_code=403, detail="You can only update your own comments")  # Только автор или админ может редактировать комментарий

    updated_comment = comment_service.update_comment(lesson_id, comment_id, user_id, comment)

    return updated_comment

# Простое удаление комментария
@router.delete("/lessons/{lesson_id}/comments/{comment_id}", summary="Soft Delete comments", tags=["Comments"])
def soft_delete_comment(lesson_id: int, comment_id: int, user_id: int, payload: TokenPayload = Depends(get_current_user)):
    existing_comment = comment_service.get_comment_by_id(comment_id, user_id)
    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if payload.user_id != existing_comment.user_id and payload.user_id != 3:
        raise HTTPException(status_code=403, detail="You can only delete your own comments")  # Только автор или админ может удалить комментарий

    deleted_comment = comment_service.soft_delete_comment(user_id, lesson_id, comment_id)

    return deleted_comment

# Сложное удаление комментария
@router.delete("/lessons/{lesson_id}/comments/{comment_id}/hard", summary="Hard Delete comments", tags=["Comments"])
def hard_delete_comment(lesson_id: int, user_id: int, comment_id: int,  payload: TokenPayload = Depends(get_current_user)):
    if payload.role_id != 3:
        raise HTTPException(status_code=403, detail="Access denied")

    comment = comment_service.hard_delete_comment(user_id, lesson_id, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return Response(json.dumps({'message': 'Comment successfully hard deleted'}),
                    status_code=200,
                    media_type='application/json'
    )