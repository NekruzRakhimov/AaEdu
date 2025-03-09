from pydantic import BaseModel


# "student" или "teacher"
class CourseUserCreate(BaseModel):
    user_id: int
    role: str

