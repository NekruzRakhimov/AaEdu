from pydantic import BaseModel
from datetime import datetime


class ScheduleSchema(BaseModel):
    course_id: int
    lesson_id: int
    mentor_id: int
    scheduled_time: datetime

    class Config:
        orm_mode = True
