from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, List
from .listitem import ListItem


class List(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str]
    created_at: datetime = Field(default_factory=datetime.now)
    closed: bool = False

    items: List[ListItem] = Relationship()
