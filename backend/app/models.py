from pydantic import BaseModel, Field
from typing import Optional, List


class Board(BaseModel):
    id: str
    name: str


class Column(BaseModel):
    id: str
    name: str
    position: int


class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    column_id: str
    order: int = Field(ge=0)


class BoardView(BaseModel):
    board: Board
    columns: List[Column]
    tasks: List[Task]


class CreateTaskRequest(BaseModel):
    title: str
    description: Optional[str] = None
    column_id: Optional[str] = None  # default to 'todo'


class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    column_id: Optional[str] = None
    new_order: Optional[int] = None
