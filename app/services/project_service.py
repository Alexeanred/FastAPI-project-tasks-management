from sqlmodel import Session, select
from uuid import UUID
from fastapi import HTTPException
from app.models import Project, User, UserProject
from app.schemas import ProjectCreate, ProjectResponse, ProjectUpdate, ProjectUserLink

# create project operation func
def create_project(session: Session, prj_data: ProjectCreate):
    # check existing project name
    existing_prj_name = session.exec(select(Project).where(Project.name == prj_data.name)).first()
    if existing_prj_name:
        raise HTTPException(status_code=400, detail="Project name already existed, please choose different name for this project.")
    # đồng bộ project data với Project model
    db_prj = Project.model_validate(prj_data)
    session.add(db_prj)
    session.commit()
    session.refresh(db_prj)
    return db_prj

# update project
def update_project(session: Session, prj_data = ProjectUpdate, prj_id = UUID ):
    db_prj = session.get(Project, prj_id)
    if not db_prj:
        raise HTTPException(status_code=404, detail="Project not Found")
    
    if prj_data.name:
        existing_prj = session.exec(select(Project).where(Project.name == prj_data.name , Project.id != prj_id)).first()
        if existing_prj:
            raise HTTPException(status_code=400, detail="Name already existed")
        db_prj.name = prj_data.name
    if prj_data.description:
        db_prj.description = prj_data.description
    
    data = prj_data.model_dump(exclude_unset=True)
    db_prj.sqlmodel_update(data)

    session.add(db_prj)
    session.commit()
    session.refresh(db_prj)
    return db_prj

# delete project
def delete_project(session: Session, prj_id: UUID):
    db_prj = session.get(Project, prj_id)
    if not db_prj:
        raise HTTPException(status_code=404, detail="Project Not Found")
    session.delete(db_prj)
    session.commit()

# get project by id
def get_project_id(session: Session, prj_id: UUID):
    db_prj = session.get(Project, prj_id)
    if not db_prj:
        raise HTTPException(status_code=404, detail="Project Not Found")
    return db_prj

# get all projects
def get_projects(session: Session, offset: int = 0, limit: int = 100):
    db_prjs = session.exec(select(Project).offset(offset).limit(limit)).all()
    return db_prjs

def assign_user_to_project(session: Session, project_id: UUID, link_data=ProjectUserLink):
    user = session.get(User, link_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")  
    
    existing_link = session.exec(select(UserProject).where(UserProject.user_id == link_data.user_id, UserProject.project_id == project_id)).first()
    if existing_link:
        raise HTTPException(status_code=400, detail="User is already assigned to this project")
    
    link = UserProject(user_id=link_data.user_id, project_id=project_id, role=link_data.role)
    session.add(link)
    session.commit()
    session.refresh(link)

    return {"message": f"User {link_data.user_id} successfully assigned to project {project_id}"}