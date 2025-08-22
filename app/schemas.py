from pydantic import BaseModel, EmailStr, ConfigDict
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
    url: str | None = None

    model_config = ConfigDict(from_attributes=True)



class UserCreate(BaseModel):
    email: EmailStr

class User(BaseModel):
    id: int
    email: EmailStr
    todos: List[Todo] = []

    model_config = ConfigDict(from_attributes=True)