from fastapi import APIRouter, Query
from app.services import create_status, update_status, delete_status, get_statuses
from uuid import UUID
from app.dependencies import SessionDep
from app.schemas import StatusCreate, StatusResponse, StatusUpdate
from typing import Annotated

router = APIRouter(prefix="/status", tags=["Status Management"])

@router.post("/", response_model=StatusResponse, status_code=201)
async def create_status_route(status_data: StatusCreate, session: SessionDep):
    return create_status(session, status_data)

@router.patch("/{status_id}", response_model=StatusResponse)
async def update_status_route(status_id: UUID, status_data: StatusUpdate, session: SessionDep ):
    return update_status(session, status_id, status_data)

@router.delete("/{status_id}", status_code=204)
async def delete_status_route(status_id: UUID, session: SessionDep):
    return delete_status(session, status_id)

@router.get("/", response_model=list[StatusResponse])
async def get_statuses_route(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    return get_statuses(session, offset, limit)