from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


class TaskOut(TaskBase):
    id: int
    done: bool

    class Config:
        orm_mode = True
