from pydantic import BaseModel, EmailStr

class TodoBase(BaseModel):
    title: str

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    title: str | None = None
    completed: bool | None = None

class Todo(TodoBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr

class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True