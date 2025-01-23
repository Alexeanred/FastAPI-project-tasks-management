from pydantic import EmailStr, ConfigDict
from datetime import datetime
from uuid import UUID
from app.models import UserBase
from sqlmodel import SQLModel

class UserCreate(UserBase):
    name: str
    email: EmailStr

class UserUpdate(UserBase):
    name: str | None = None
    email: EmailStr | None = None

class UserProjectLink(SQLModel):
    project_id: UUID
    role: str | None = None

class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    projects: list[UserProjectLink] = []

    model_config = ConfigDict(from_attributes=True)

# user có dùng chung là name, email
# table user co id, create, update time, fk den task, fk den proj
# user create co name, email
# user update: name, email
# user prj link: prj_id, role
# res: id, time, prj, name, email