from fastapi import APIRouter, Query
from app.services import create_project, update_project, delete_project, get_project_id, get_projects, assign_user_to_project
from uuid import UUID
from app.dependencies import SessionDep
from app.schemas import ProjectCreate, ProjectResponse, ProjectUpdate, ProjectUserLink
from typing import Annotated

router = APIRouter(prefix="/projects", tags = ["Projects Management"])
# tạo prj mới
@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project_route(prj_data: ProjectCreate, session: SessionDep):
    return create_project(session, prj_data)
# update prj
@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project_route(project_id: UUID, prj_data: ProjectUpdate, session: SessionDep ):
    return update_project(session, prj_data, project_id)
# xóa prj
@router.delete("/{project_id}", status_code=204)
async def delete_project_route(project_id: UUID, session: SessionDep):
    return delete_project(session, project_id)
# lấy prj theo id
@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project_by_id_route(project_id: UUID, session: SessionDep):
    return get_project_id(session, project_id)
# lấy danh sách prj
@router.get("/", response_model=list[ProjectResponse])
async def get_projects_route(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    return get_projects(session, offset, limit)
# gán user vào prj
@router.post("/{project_id}/assign_user",response_model=dict)
def assign_user_to_project_route(session: SessionDep, project_id: UUID, link_data: ProjectUserLink):
    return assign_user_to_project(session, project_id, link_data)
