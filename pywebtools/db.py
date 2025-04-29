from sqlalchemy import create_engine
from sqlmodel import Session

engine = create_engine("sqlite:///data.db", echo=True)
session = Session(engine)
