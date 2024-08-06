
from fastapi import FastAPI
from app.api.v1.endpoints import tasks
from app.core.config import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tasks.router, prefix='/api/v1')

