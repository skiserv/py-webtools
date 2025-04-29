from flask import Flask
from flask import render_template
from sqlmodel import SQLModel
from sqlmodel import select

from pywebtools.models.note import Note
from pywebtools.db import session

from pywebtools.routers.notes import notes_router
from pywebtools.routers.lists import lists_router


app = Flask(__name__)
app.jinja_env.add_extension("jinja_markdown.MarkdownExtension")
app.register_blueprint(notes_router, url_prefix="/notes")
app.register_blueprint(lists_router, url_prefix="/lists")


@app.get("/")
def index():
    return render_template("index.html")
