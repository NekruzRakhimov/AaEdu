from pydantic import BaseModel


class LessonSchema(BaseModel):
    title: str
    description: str
    content: str
