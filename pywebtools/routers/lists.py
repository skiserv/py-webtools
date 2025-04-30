from uuid import UUID

from flask import Blueprint, render_template, request, abort
from sqlmodel import Session, select

from pywebtools.db import session
from pywebtools.models.list import List
from pywebtools.models.listitem import ListItem

lists_router = Blueprint("lists", __name__)


@lists_router.get("/")
def lists():
    lists = {}
    stmt = select(List)
    lists = session.exec(stmt)
    return render_template("lists/lists.html", lists=lists)


@lists_router.post("/")
def create_list():
    new_list = List(name=request.form["name"], description=request.form["description"])
    session.add(new_list)
    session.commit()
    session.refresh(new_list)
    return render_template("lists/list-inline.html", list=new_list)


@lists_router.get("/<uuid:list_id>")
def list(list_id: UUID):
    l = session.get(List, list_id)
    if not l:
        abort(404)
    return render_template("lists/list.html", list=l)


@lists_router.post("/<uuid:list_id>/items")
def create_item(list_id: UUID):
    l = session.get(List, list_id)
    if not l:
        abort(404)
    item = ListItem(content=request.form["content"], list_id=l.id)
    session.add(item)
    session.commit()
    session.refresh(item)
    return render_template("lists/list-item.html", item=item)


@lists_router.delete("/<uuid:list_id>/items/<uuid:item_id>")
def delete_item(list_id: UUID, item_id:UUID):
    item = session.get(ListItem, item_id)
    if not item or item.list_id != list_id:
        abort(404)
    session.delete(item)
    session.commit()
    return ""