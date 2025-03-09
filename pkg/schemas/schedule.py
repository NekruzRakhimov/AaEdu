from pydantic import BaseModel
from datetime import datetime

class ScheduleCreate(BaseModel):
    lesson_id: int
    teacher_id: int
    scheduled_time: datetime

class ScheduleUpdate(BaseModel):
    scheduled_time: datetime
