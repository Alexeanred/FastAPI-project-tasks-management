from app.models import ProjectBase, Project
from uuid import UUID
from sqlmodel import SQLModel
from pydantic import ConfigDict
# ProjectCreate, ProjectUpdate, Response

class ProjectCreate(ProjectBase):
    name: str # bat buoc co name
    description: str | None = None # co hoac khong description deu dc

class ProjectUpdate(ProjectBase):
    name: str | None = None # optional, default = None
    description: str | None = None # optional, default= None

class ProjectUserLink(SQLModel):
    user_id: UUID
    role: str | None = None  

class ProjectResponse(ProjectBase):
    id: UUID # trả về thêm id, đã có name và description.
    users: list[ProjectUserLink] = []

    model_config = ConfigDict(from_attributes=True)
