from fastapi import APIRouter, Query
from app.services import create_task, update_task, delete_tasks, get_tasks, allocate_task_user
from uuid import UUID, uuid4
from app.dependencies import SessionDep
from app.schemas import TaskCreate, TaskFilter, TaskResponse, TaskUpdate, TaskAllocation
from typing import Annotated, List

router = APIRouter(prefix="/task", tags = ["Tasks Management"])

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task_route(session: SessionDep, task_data: TaskCreate):
    return create_task(session, task_data)

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task_route(session: SessionDep, task_id: UUID, task_data: TaskUpdate):
    return update_task(session, task_id, task_data)

@router.delete("/") 
async def delete_tasks_route(session: SessionDep, task_ids: Annotated[list[UUID],Query(description="List of task IDs to delete")]):
    return delete_tasks(session, task_ids)

@router.get("/", response_model=list[TaskResponse])
async def get_tasks_route(
    session: SessionDep,
    project_id: str | None = Query(None, description="Filter by project ID"),
    user_id: str | None = Query(None, description="Filter by user ID"),
    status_id: str | None = Query(None, description="Filter by status ID"),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,   
):
    filters = {"project_id": project_id, "user_id": user_id, "status_id": status_id}
    return get_tasks(session, filters, offset, limit)

@router.patch("/{task_id}/assign_user", response_model=TaskResponse)
async def assign_user_to_task_route(session: SessionDep, task_id: UUID, allocation_data: TaskAllocation):
    return allocate_task_user(session, task_id, allocation_data.user_id)



