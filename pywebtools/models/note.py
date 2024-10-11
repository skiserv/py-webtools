from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from .listitem import ListItem


class Note(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    content: Optional[str]
    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)
