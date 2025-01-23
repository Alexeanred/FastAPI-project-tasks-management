# task: id, name, description, deadline
# fk: prj_id, user_id, status_id
# Relationship

# tasks and projects: one to many
# tasks and users: one to many
# tasks and status: one to many
# users and projects: one to many

# Base: name, des, deadline
# table: id, prj_id, user_id, status_id, relationship

from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from pydantic import field_validator

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.user import User
    from app.models.status import Status

class TaskBase(SQLModel):
    name: str = Field(index=True)
    description: str | None = Field(default=None)
    deadline: datetime = Field(index=True)

class Task(TaskBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)

    # project: 1 task phải có project, 1 project có nhiều tasks
    project_id: UUID = Field(foreign_key="project.id")
    project: Optional["Project"] = Relationship(back_populates="tasks")

    # user: 1 task phải có user làm hoặc ko, 1 user có thể có nhiều tasks
    user_id: UUID | None = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="tasks")

    # status: 1 task có 1 status, 1 status có thể nhiều tasks gắn vào
    status_id: UUID = Field(foreign_key="status.id")
    status: Optional["Status"] = Relationship(back_populates="tasks")

