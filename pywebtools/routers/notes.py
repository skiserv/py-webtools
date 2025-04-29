from uuid import UUID

from flask import Blueprint, render_template, request
from sqlmodel import Session, select

from pywebtools.db import session
from pywebtools.models.note import Note


notes_router = Blueprint("notes", __name__)


@notes_router.get("/")
def notes():
    stmt = select(Note)
    notes = session.exec(stmt)
    return render_template("notes/notes.html", notes=notes)


@notes_router.post("/")
def create_note():
    note = Note(name=request.form["name"], content=request.form["content"])
    session.add(note)
    session.commit()
    return render_template("notes/note.html", note=note)


@notes_router.patch("/<uuid:note_id>")
def edit_note(note_id: str):
    note = session.get(Note, note_id)
    note.name = request.form["name"]
    note.content = request.form["content"]
    session.add(note)
    session.commit()
    return render_template("notes/note.html", note=note)


@notes_router.get("/<uuid:note_id>/edit")
def edit_form(note_id: UUID):
    note = session.get(Note, note_id)
    return render_template("notes/note-edit.html", note=note)
