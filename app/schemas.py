from pydantic import BaseModel, EmailStr
from typing import List

class TodoBase(BaseModel):
    title: str

class TodoCreate(TodoBase):
    user_id: int

class TodoUpdate(TodoBase):
    title: str | None = None
    completed: bool | None = None

class Todo(TodoBase):
    id: int
    completed: bool
    user_id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr

class User(BaseModel):
    id: int
    email: EmailStr
    todos: List[Todo] = []

    class Config:
        orm_mode = True