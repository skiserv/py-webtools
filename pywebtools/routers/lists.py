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
from pywebtools.models.list import List
from pywebtools.models.listitem import ListItem
from pywebtools.templating import templates

router = APIRouter(
    prefix="/lists",
    tags=["lists"],
    dependencies=[],
)


@router.get("/", response_class=HTMLResponse)
async def lists(request: Request, session: Session = Depends(get_session)):
    lists = {}
    stmt = select(List)
    lists = session.exec(stmt)
    return templates.TemplateResponse(
        request=request, name="lists/lists.html", context={"lists": lists}
    )


@router.post("/", response_class=HTMLResponse)
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


@router.get("/{list_id}", response_class=HTMLResponse)
async def list(
    request: Request,
    list_id: UUID,
    session: Session = Depends(get_session),
):
    return templates.TemplateResponse(
        request=request,
        name="lists/list.html",
        context={"list": session.get(List, list_id)},
    )


@router.post("/{list_id}/items", response_class=HTMLResponse)
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
