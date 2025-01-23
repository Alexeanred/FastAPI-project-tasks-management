from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr
from datetime import datetime
from uuid import UUID, uuid4
from typing import TYPE_CHECKING, Optional, List
from app.models.project import UserProject
if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.project import Project, UserProject
# task: create User, Update User, Delete User
# id, name, email, create_at, updated_at
# create User: name, email
# update User: name, email
# delete User: email
class UserBase(SQLModel):
    name: str | None = None
    email: EmailStr | None = Field(default=None, unique=True)

class User(UserBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # 1 user có thể nhiều tasks
    tasks: List["Task"] = Relationship(back_populates="user")
    # 1 user có thể tham gia nhiều projects
    projects: List["UserProject"] = Relationship(back_populates="user")


# user có dùng chung là name, email
# table user co id, create, update time, fk den task, fk den proj
# user create co name, email
# user update: name, email
# user prj link: prj_id, role
# res: id, time, prj, name, email
