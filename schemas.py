from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = ""

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    completed: bool

class Todo(TodoBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True