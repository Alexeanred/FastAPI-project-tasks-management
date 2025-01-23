from fastapi import FastAPI
from app.routers import users_router, projects_router, status_router, tasks_router
from sqlmodel import SQLModel
from app.database import engine
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
    # Tắt: Nếu cần thêm xử lý
    print("Cleaning up resources...")

app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(projects_router)
app.include_router(status_router)
app.include_router(tasks_router)
