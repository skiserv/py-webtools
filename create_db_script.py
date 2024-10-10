from sqlmodel import create_engine, SQLModel
from pywebtools.models.list import List
from pywebtools.models.listitem import ListItem

engine = create_engine("sqlite:///data.db")
SQLModel.metadata.create_all(engine)
