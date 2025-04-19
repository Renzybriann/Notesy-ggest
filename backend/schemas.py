# backend/schemas.py

from pydantic import BaseModel
from typing import List, Optional

class NoteCreate(BaseModel):
    content: str
    subtasks: Optional[List[str]] = []

class NoteRead(NoteCreate):
    id: int

    class Config:
        from_attributes = True  # Use 'from_attributes' instead of 'orm_mode'
