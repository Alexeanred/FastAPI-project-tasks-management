from sqlmodel import Session, select
from uuid import UUID
from fastapi import HTTPException
from app.models import User
from datetime import datetime
from app.schemas import UserCreate, UserUpdate

def create_user(session: Session, user_data: UserCreate):
    # check email
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # đồng bộ user_data với User model
    db_user = User.model_validate(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)  # Lấy lại dữ liệu mới nhất từ database
    return db_user

def update_user(session: Session, user_id: UUID, user_data: UserUpdate):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_data.name:
        user_db.name = user_data.name
    if user_data.email:
        existing_user = session.exec(select(User).where(User.email == user_data.email, User.id != user_id)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already used by another user")  
        user_db.email = user_data.email
    user_db.updated_at = datetime.utcnow()
    data = user_data.model_dump(exclude_unset=True)
    # only the data sent by the client, excluding any values that would be there just for being the default values.
    user_db.sqlmodel_update(data) # update the user_db with the data from data
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db   

def delete_user(session: Session, user_id: UUID):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()    

def get_user_projects(session: Session, user_id: UUID):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    projects_and_roles = [
        {"project_id" : link.project_id, "project_name":  link.project.name,"role": link.role} for link in user.projects
    ]

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "projects": projects_and_roles
    }   
   