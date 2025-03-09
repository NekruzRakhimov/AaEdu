from pydantic import BaseModel


class UserSchema(BaseModel):
    full_name: str
    username: str
    password: str
    birth_date: str


class UserSignInSchema(BaseModel):
    username: str
    password: str
