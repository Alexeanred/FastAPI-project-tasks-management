from sqlmodel import Session, select
from uuid import UUID
from fastapi import HTTPException
from app.models import Task
from datetime import datetime, timezone
from app.schemas import TaskResponse, TaskCreate, TaskFilter, TaskUpdate, TaskAllocation
from app.models import Project, Status, User
from app.dependencies import SessionDep
import logging
# create task
def create_task(session: Session, task_data: TaskCreate):
    # check project ton tai
    project = session.get(Project, task_data.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project Not Found.")
    
    # check status ton tai
    status = session.get(Status, task_data.status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Status Not Found")

    # check user
    user = None
    if task_data.user_id:
        user = session.get(User, task_data.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    
    # check deadline
    if task_data.deadline:
        # Convert to UTC if the datetime is offset-naive
        if task_data.deadline.tzinfo is None:
            task_data.deadline = task_data.deadline.replace(tzinfo=timezone.utc)
        # Check if deadline is in the past
        if task_data.deadline < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Deadline must be in the future.")
    
    # tạo task
    db_task = Task.model_validate(task_data)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

# update task
def update_task(session: Session, task_id: UUID, task_data: TaskUpdate):
    # check task id exist
    task_db = session.get(Task, task_id)
    if not task_db:
        raise HTTPException(status_code=404, detail="Task not found.")
            
    # check status
    status = None
    if task_data.status_id:
        status = session.get(Status, task_data.status_id)
        if not status:
            raise HTTPException(status_code=404, detail="Status not found")
    task_db.status_id = task_data.status_id
    # check deadline
    if task_data.deadline:
        # Convert to UTC if the datetime is offset-naive
        if task_data.deadline.tzinfo is None:
            task_data.deadline = task_data.deadline.replace(tzinfo=timezone.utc)
        # Check if deadline is in the past
        if task_data.deadline < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Deadline must be in the future.")
    task_db.deadline = task_data.deadline
    # name
    if task_data.name:
        task_db.name = task_data.name
    
    # description
    if task_data.description:
        task_db.description = task_data.description
    
    # update task
    data = task_data.model_dump(exclude_unset=True)
    task_db.sqlmodel_update(data)
    session.add(task_db)
    session.commit()
    session.refresh(task_db)
    return task_db 

# delete task
def delete_tasks(session: Session, task_ids: list[UUID]):
    # kiem tra TH ko co tasks nao found
    tasks = session.exec(select(Task).where(Task.id.in_(task_ids))).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found.")

    # kiem tra task_id bi miss ko
    found_task_ids = {task.id for task in tasks}
    missing_task_ids = set(task_ids) - found_task_ids
    if missing_task_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Tasks not found for IDs: {', '.join(str(task_id) for task_id in missing_task_ids)}"
        ) 

    for task in tasks:
        session.delete(task)
    
    session.commit()
    return {"message": "Tasks deleted successfully", "deleted_task_ids": list(found_task_ids)}

# read task
def get_tasks(session: Session, filters: dict, offset: int = 0, limit: int = 100):
    # lấy Task từ db
    query = select(Task)
    # Lọc dữ liệu
    if filters.get("project_id"):
        query = query.where(Task.project_id == filters["project_id"])
    if filters.get("user_id"):
        query = query.where(Task.user_id == filters["user_id"])
    if filters.get("status_id"):
        query = query.where(Task.status_id == filters["status_id"])
    # exec
    tasks = session.exec(query.offset(offset).limit(limit)).all()

    return tasks

# phân công task
def allocate_task_user(session: Session, task_id: UUID, user_id: UUID):
    # Lấy task từ database
    task_db = session.get(Task, task_id)
    if not task_db:
        raise HTTPException(status_code=404, detail="Task not found.")

    # Kiểm tra và gán user_id
    try:
        task_db.user_id = UUID(str(user_id))  # Đảm bảo user_id là kiểu UUID
    except ValueError:
        logging.error(f"Invalid UUID format for user_id: {user_id}")
        raise HTTPException(status_code=400, detail="Invalid UUID format for user_id.")

    # Commit các thay đổi
    session.add(task_db)
    session.commit()
    session.refresh(task_db)

    return task_db




