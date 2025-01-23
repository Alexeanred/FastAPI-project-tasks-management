from fastapi import APIRouter
from app.services import create_user, delete_user, update_user, get_user_projects
from uuid import UUID
from app.dependencies import SessionDep
from app.schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users Management"])
# tạo user mới
@router.post("/", response_model=UserResponse, status_code=201)
async def create_user_route(user_data: UserCreate, session: SessionDep):
    return create_user(session, user_data)
# update user
@router.patch("/{user_id}", response_model=UserResponse)
async def update_user_route(user_id: UUID, user_data: UserUpdate, session: SessionDep):
    return update_user(session, user_id, user_data)
# lấy danh sách project của user
@router.get("/{user_id}/projects", response_model=dict)
def get_user_projects_route(user_id: UUID, session: SessionDep):
    return get_user_projects(session, user_id)
# xóa user
@router.delete("/{user_id}", status_code=204)
async def delete_user_route(user_id: UUID, session: SessionDep):
    return delete_user(session, user_id)
