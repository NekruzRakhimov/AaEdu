from pydantic import BaseModel, condecimal
from typing import Optional


class HomeworkSchema(BaseModel):
    lesson_id: int
    student_id: int
    score: condecimal(max_digits=5, decimal_places=2)


class HomeworkUpdateSchema(BaseModel):
    score: condecimal(max_digits=5, decimal_places=2)


class HomeworkResponseSchema(HomeworkSchema):
    id: int
    mentor_id: int

    class Config:
        from_attributes = True
