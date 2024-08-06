from pydantic import BaseModel
from typing import List, Optional


class RequestBase(BaseModel):
    a: int
    b: int


class TaskCreate(RequestBase):
    pass


class RequestCreate(RequestBase):
    pass


class Request(RequestBase):
    id: int
    result: Optional[int] = None
    status: str

    class Config:
        orm_mode = True


class MultipleTasksCreate(BaseModel):
    tasks: List[TaskCreate]