from sqlmodel import create_engine, SQLModel
from pywebtools.models.list import List
from pywebtools.models.listitem import ListItem
from pywebtools.models.note import Note

engine = create_engine("sqlite:///data.db")
SQLModel.metadata.create_all(engine)
