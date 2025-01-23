from app.models import TaskBase, Task
from uuid import UUID
from datetime import datetime, timezone
from sqlmodel import SQLModel
# bat buoc nhap prj, status, optional user
class TaskCreate(TaskBase):
    project_id: UUID
    status_id: UUID
    user_id: UUID | None = None
    
# optional cho phép cập nhật các field
class TaskUpdate(TaskBase):
    name: str | None = None
    description: str | None = None
    deadline: datetime | None = None
    status_id: UUID | None = None   

# 
# class TaskDelete(SQLModel):
#     task_ids: list[UUID]

class TaskFilter(SQLModel):
    project_id: UUID | None = None
    user_id: UUID | None = None
    status_id: UUID | None = None

class TaskResponse(TaskBase):
    id: UUID
    project_id: UUID
    user_id: UUID | None = None
    status_id: UUID

class TaskAllocation(SQLModel):
    user_id: UUID
