# app/crud.py
from sqlalchemy.orm import Session
from . import models

def get_note(db: Session, note_id: int):
    return db.query(models.Note).filter(models.Note.id == note_id).first()

def get_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Note).offset(skip).limit(limit).all()

def create_note(db: Session, title: str, content: str):
    note = models.Note(title=title, content=content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def update_note(db: Session, note_id: int, title: str, content: str):
    note = get_note(db, note_id)
    if not note:
        return None
    note.title = title
    note.content = content
    db.commit()
    db.refresh(note)
    return note

def delete_note(db: Session, note_id: int):
    note = get_note(db, note_id)
    if not note:
        return False
    db.delete(note)
    db.commit()
    return True
