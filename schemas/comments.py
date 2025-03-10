from pydantic import BaseModel
import datetime

class CommentSchema(BaseModel):
    id: int
    lesson_id: int
    user_id: int
    content: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    is_deleted: bool
