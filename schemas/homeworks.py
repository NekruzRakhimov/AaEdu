from pydantic import BaseModel, condecimal
from datetime import datetime


class HomeworkBase(BaseModel):
    lesson_id: int
    student_id: int
    score: condecimal(max_digits=5, decimal_places=2)


class HomeworkCreate(HomeworkBase):
    pass


class HomeworkResponse(HomeworkBase):
    id: int
    submission_date: datetime
