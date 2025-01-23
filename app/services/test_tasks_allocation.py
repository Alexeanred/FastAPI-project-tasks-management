from sqlmodel import Session,create_engine
from app.dependencies import SessionDep
from app.models import Task, User  # Import các model cần thiết

DATABASE_URL = "postgresql://duytien:okbaby@localhost:5432/task_management_db"
engine = create_engine(DATABASE_URL)

def SessionDep():
    return Session(engine)

# def create_and_update_task():
#     with SessionDep() as session:
#         # Step 1: Tạo một task mới mà không có user_id
#             new_task = Task(name="Task kho", description="This is a task", deadline="2025-01-24T03:10:18.353Z", project_id="73a6f0b1-0c2a-4ae3-9b26-411252e5d9a9", status_id="3ed0f56c-5781-478a-b5fc-94dddd563b31", user_id ="a2fbc806-8db2-4e6a-a30d-714840e6718c")
#             session.add(new_task)
#             session.commit()
#             session.refresh(new_task)  # Refresh để lấy giá trị mới từ database

#             print(f"Task created: {new_task.id}, user_id: {new_task.user_id}")

#             # Step 2: Tạo một user mới
#             new_user = User(name="Sample User 2", email="hunglamdasdaaew@example.com")
#             session.add(new_user)
#             session.commit()
#             session.refresh(new_user)

#             print(f"User created: {new_user.id}")

#             # Step 3: Cập nhật user_id của task
#             new_task.user_id = new_user.id
#             session.commit()
#             session.refresh(new_task)

#             print(f"Task updated: {new_task.id}, user_id: {new_task.user_id}")

# create_and_update_task()

# ket luan: user id phai co trong table user, co the update duoc null va user id cu o bang task.

from app.services import allocate_task_user
from uuid import UUID
from app.schemas import TaskAllocation

with SessionDep() as session:
    allocate_task_user(session, UUID("9259ea0f-213b-4cf4-8326-ef8344e95665"), user_id=UUID("3b21e04d-9d05-4314-a240-5f39492bc92a"))