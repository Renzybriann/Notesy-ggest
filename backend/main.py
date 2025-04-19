from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os
import re

from utils.gemini import generate_subtasks_with_gemini
from database import SessionLocal, engine
from models import Base, NoteModel

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    raise ValueError("API_KEY not found in .env")

# Create tables in database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request
class NoteCreate(BaseModel):
    content: str

# Pydantic model for response
class NoteResponse(BaseModel):
    id: int
    content: str
    subtasks: List[str]

    class Config:
        orm_mode = True

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Clean subtasks
def clean_subtasks(subtasks: List[str]) -> List[str]:
    return [re.sub(r'\*\*.*?\*\*', '', subtask).strip() for subtask in subtasks]

# Create note
@app.post("/notes", response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    subtasks = generate_subtasks_with_gemini(note.content)
    cleaned_subtasks = clean_subtasks(subtasks)

    new_note = NoteModel(content=note.content, subtasks=cleaned_subtasks)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

# Get all notes
@app.get("/notes", response_model=List[NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    return db.query(NoteModel).all()

# Delete note by ID
@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted", "note": note.content}
