from fastapi import FastAPI, Request, Form, Depends, Path
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pywebtools.models.listitem import ListItem
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pywebtools.models.list import List

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

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
        request=request, name="lists.html", context={"lists": lists}
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
        request=request, name="list-inline.html", context={"list": new_list}
    )


@app.get("/lists/{list_id}", response_class=HTMLResponse)
async def list(
    request: Request,
    list_id: int,
    session: Session = Depends(get_session),
):
    return templates.TemplateResponse(
        request=request, name="list.html", context={"list": session.get(List, list_id)}
    )


@app.post("/lists/{list_id}/items", response_class=HTMLResponse)
async def create_item(
    request: Request,
    list_id: int,
    session: Session = Depends(get_session),
    content: str = Form(),
):
    item = ListItem(content=content, list_id=session.get(List, list_id).id)
    session.add(item)
    session.commit()
    session.refresh(item)
    return templates.TemplateResponse(
        request=request, name="list-item.html", context={"item": item}
    )
