# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <-- add this
from sqlalchemy.orm import Session
from . import models, crud
from .database import SessionLocal, engine, Base
from pydantic import BaseModel

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CORS Middleware ---
origins = [
    "http://localhost:5173",  # React dev server http://localhost:5173 https://mayur.themayur.com
    # Add your production frontend URL here later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # allow only these origins
    allow_credentials=True,
    allow_methods=["*"],         # GET, POST, PUT, DELETE
    allow_headers=["*"],         # all headers
)

# --- Pydantic schemas ---
class NoteCreate(BaseModel):
    title: str
    content: str | None = None

class NoteOut(NoteCreate):
    id: int

# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CRUD endpoints ---
@app.get("/notes", response_model=list[NoteOut])
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_notes(db, skip=skip, limit=limit)

@app.post("/notes", response_model=NoteOut)
def create_note(note_in: NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db, title=note_in.title, content=note_in.content)

@app.get("/notes/{note_id}", response_model=NoteOut)
def read_note(note_id: int, db: Session = Depends(get_db)):
    note = crud.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.put("/notes/{note_id}", response_model=NoteOut)
def update_note(note_id: int, note_in: NoteCreate, db: Session = Depends(get_db)):
    note = crud.update_note(db, note_id, note_in.title, note_in.content)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.delete("/notes/{note_id}")
def delete_note_endpoint(note_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_note(db, note_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"ok": True}
