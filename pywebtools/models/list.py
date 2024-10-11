from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from .listitem import ListItem


class List(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: Optional[str]
    created_at: datetime = Field(default_factory=datetime.now)
    closed: bool = False

    items: List[ListItem] = Relationship()
