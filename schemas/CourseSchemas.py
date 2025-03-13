from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CourseSchema(BaseModel):
    name: str
    price: int
    description: str
