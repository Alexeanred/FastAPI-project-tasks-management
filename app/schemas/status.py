from app.models import StatusBase, Status
from uuid import UUID

class StatusCreate(StatusBase):
    pass

class StatusUpdate(StatusBase):
    status: str | None = None

class StatusResponse(StatusBase):
    id: UUID

