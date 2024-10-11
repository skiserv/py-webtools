from fastapi import FastAPI, Request, Form, Depends, Path
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pywebtools.models.listitem import ListItem
from pywebtools.models.note import Note
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pywebtools.models.list import List
from uuid import UUID

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(
    directory="templates",
    extensions={"jinja_markdown.MarkdownExtension"},
)

engine = create_engine("sqlite:///data.db")


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/lists/", response_class=HTMLResponse)
async def lists(request: Request, session: Session = Depends(get_session)):
    lists = {}
    stmt = select(List)
    lists = session.exec(stmt)
    return templates.TemplateResponse(
        request=request, name="lists/lists.html", context={"lists": lists}
    )


@app.post("/lists/", response_class=HTMLResponse)
async def create_list(
    request: Request,
    session: Session = Depends(get_session),
    name: str = Form(),
    description: str = Form(),
):
    new_list = List(name=name, description=description)
    session.add(new_list)
    session.commit()
    session.refresh(new_list)
    return templates.TemplateResponse(
        request=request, name="lists/list-inline.html", context={"list": new_list}
    )


@app.get("/lists/{list_id}", response_class=HTMLResponse)
async def list(
    request: Request,
    list_id: UUID,
    session: Session = Depends(get_session),
):
    return templates.TemplateResponse(
        request=request, name="lists/list.html", context={"list": session.get(List, list_id)}
    )


@app.post("/lists/{list_id}/items", response_class=HTMLResponse)
async def create_item(
    request: Request,
    list_id: UUID,
    session: Session = Depends(get_session),
    content: str = Form(),
):
    item = ListItem(content=content, list_id=session.get(List, list_id).id)
    session.add(item)
    session.commit()
    session.refresh(item)
    return templates.TemplateResponse(
        request=request, name="lists/list-item.html", context={"item": item}
    )


@app.get("/notes/", response_class=HTMLResponse)
async def notes(request: Request, session: Session = Depends(get_session)):
    stmt = select(Note)
    notes = session.exec(stmt)
    return templates.TemplateResponse(
        request=request, name="notes/notes.html", context={"notes": notes}
    )


@app.post("/notes/", response_class=HTMLResponse)
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
