from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.user import User
# from .task import Task

# field: id, name, description

# tạo table UserProject thể hiện mqh many many
class UserProject(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)
    project_id: UUID = Field(foreign_key="project.id", primary_key=True)
    role: str | None = Field(default=None, index=True)
    
    user: "User" = Relationship(back_populates="projects")
    project: "Project" = Relationship(back_populates="users")
# tạo base có name (index) và description (optional)
class ProjectBase(SQLModel):
    name: str = Field(index=True)
    description: str | None = Field(default=None)

# tạo table project có thêm id
class Project(ProjectBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)

    # 1 project có nhiều tasks
    tasks: List["Task"] = Relationship(back_populates="project")
    # 1 project có nhiều users
    users: list["UserProject"] = Relationship(back_populates="project")



