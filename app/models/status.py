from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from typing import TYPE_CHECKING, List
# field: id, status
if TYPE_CHECKING:
    from app.models.task import Task

class StatusBase(SQLModel):
    status: str = Field(index=True, unique=True)

class Status(StatusBase, table= True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)

    tasks: List["Task"] = Relationship(back_populates="status")
    


