from pydantic import BaseModel
import datetime

class CommentSchema(BaseModel):
    user_id: int
    content: str

    class Config:
        from_attributes = True