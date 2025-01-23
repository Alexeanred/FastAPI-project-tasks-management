from sqlmodel import Session, select
from uuid import UUID
from fastapi import HTTPException
from app.models import Status
from app.schemas import StatusResponse, StatusCreate, StatusUpdate

# create status
def create_status(session: Session, status_data: StatusCreate):
    existing_status = session.exec(select(Status).where(Status.status == status_data.status)).first()
    if existing_status:
        raise HTTPException(status_code=400, detail="Status already exists.")

    status = Status.model_validate(status_data)
    session.add(status)
    session.commit()
    session.refresh(status)
    return status

# update status
def update_status(session: Session, status_id: UUID, status_data: StatusUpdate):
    db_status = session.get(Status, status_id)
    # check status tồn tại
    if not db_status:
        raise HTTPException(status_code=404, detail="Status not found.")
    # check status name da co chua
    if status_data.status:
        existing_status = session.exec(select(Status).where(Status.status == status_data.status)).first()
        if existing_status:
            raise HTTPException(status_code=400, detail="Status already exists.")
    
    data = status_data.model_dump(exclude_unset=True)
    db_status.sqlmodel_update(data)

    session.add(db_status)
    session.commit()
    session.refresh(db_status)
    return db_status

def delete_status(session: Session, status_id: UUID):
    db_status = session.get(Status, status_id)
    if not db_status:
        raise HTTPException(status_code=404, detail="Status not found.")
    
    session.delete(db_status)
    session.commit()

def get_statuses(session: Session, offset: int = 0, limit: int = 100):
    return session.exec(select(Status).offset(offset).limit(limit)).all()