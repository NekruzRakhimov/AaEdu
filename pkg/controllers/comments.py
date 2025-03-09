import datetime
import json

from fastapi import APIRouter, Depends, status
from starlette.responses import Response
from sqlalchemy.orm import Session

from pkg.controllers.middlewares import get_current_user
from schemas.comments import CreateComment, CommentUpdate, CommentResponse


from db.models import Comment, Lesson, User
from db.postgres import get_db

router = APIRouter()

# Создание комментария
@router.post("/comments/")
async def create_comment(comment: CreateComment, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    lesson = db.query(Lesson).filter(Lesson.id == comment.lesson_id).first()
    if not lesson:
       return Response(json.dumps({'error': 'lesson not found'}), status.HTTP_404_NOT_FOUND)

    new_comment = Comment(
        lesson_id=comment.lesson_id,
        user_id=user.id,
        content=comment.content,
        created_at=datetime.datetime.now(),
        update_at=datetime.datetime.now()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# Получение списка комментариев к уроку
@router.get("/comments/{lesson_id}", response_model=list[CommentResponse])
async def get_comments(lesson_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.lesson_id == lesson_id).all()
    return comments.limit(limit).offset(offset).all()

# Редактирование комментария
@router.put("/comments/{comment_id}")
async def update_comment(comment_id: int, comment: CommentUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    comment_to_update = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == user.id).first()
    if not comment_to_update:
        return Response(json.dumps({'error': 'comment not found'}), status.HTTP_404_NOT_FOUND)

    comment_to_update.content = comment.content
    comment_to_update.update_at = datetime.datetime.now()
    db.commit()
    db.refresh(comment_to_update)
    return comment_to_update

# Удаление комментария (мягкое удаление)
@router.delete("/comments/{comment_id}")
async def delete_comment(comment_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    comment_to_delete = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == user.id).first()
    if not comment_to_delete:
        return Response(json.dumps({'error': 'comment not found'}), status.HTTP_404_NOT_FOUND)

    db.delete(comment_to_delete)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
