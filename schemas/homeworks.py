from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HomeworkBase(BaseModel):
    lesson_id: int
    student_id: int
    score: float

class HomeworkCreate(HomeworkBase):
    mentor_id: int

class HomeworkResponse(HomeworkBase):
    id: int
    submission_date: datetime

    class Config:
        from_attributes = True
