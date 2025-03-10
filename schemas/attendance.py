from datetime import datetime

from pydantic import BaseModel


class AttendanceSchema(BaseModel):
    user_id: int
    lesson_id: int
    attended: bool
    attendance_date: datetime
