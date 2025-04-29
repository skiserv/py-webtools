from uuid import UUID

from flask import Blueprint, render_template, request
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
def list():
    return render_template(
        "lists/list.html",
        list=session.get(List, list_id),
    )


@lists_router.post("/<list_id>/items")
def create_item():
    item = ListItem(
        content=request.form["content"], list_id=session.get(List, list_id).id
    )
    session.add(item)
    session.commit()
    session.refresh(item)
    return render_template("lists/list-item.html", item=item)
