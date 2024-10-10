from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional


class ListItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

    list_id: Optional[int] = Field(default=None, foreign_key="list.id")
