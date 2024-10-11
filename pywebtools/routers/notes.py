from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    FastAPI,
    Request,
    Form,
    Depends,
    Path,
)
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from pywebtools.db import get_session
from pywebtools.models.note import Note
from pywebtools.templating import templates


router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    dependencies=[],
)


@router.get("/", response_class=HTMLResponse)
async def notes(request: Request, session: Session = Depends(get_session)):
    stmt = select(Note)
    notes = session.exec(stmt)
    return templates.TemplateResponse(
        request=request, name="notes/notes.html", context={"notes": notes}
    )


@router.post("/", response_class=HTMLResponse)
async def create_note(
    request: Request,
    session: Session = Depends(get_session),
    name: str = Form(),
    content: str = Form(),
):
    note = Note(name=name, content=content)
    session.add(note)
    session.commit()
    return templates.TemplateResponse(
        request=request, name="notes/note.html", context={"note": note}
    )


@router.patch("/{note_id}", response_class=HTMLResponse)
async def edit_note(
    note_id: UUID,
    request: Request,
    name: str = Form(),
    content: str = Form(),
    session: Session = Depends(get_session),
):
    note = session.get(Note, note_id)
    note.name = name
    note.content = content
    session.add(note)
    session.commit()
    return templates.TemplateResponse(
        request=request, name="notes/note.html", context={"note": note}
    )


@router.get("/{note_id}/edit", response_class=HTMLResponse)
async def edit_form(
    note_id: UUID, request: Request, session: Session = Depends(get_session)
):
    note = session.get(Note, note_id)
    return templates.TemplateResponse(
        request=request, name="notes/note-edit.html", context={"note": note}
    )
