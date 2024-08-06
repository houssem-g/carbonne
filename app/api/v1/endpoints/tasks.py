from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.request import TaskCreate, Request, MultipleTasksCreate
from app.crud import request as crud_request
from app.tasks.multiply import multiply  # Import de la tâche directement
from celery.result import AsyncResult

router = APIRouter()

def call_celery_task(db_request_id: int):
    task_result = multiply.delay(db_request_id)
    return task_result.id

@router.post('/submit_task/', response_model=dict)
async def submit_task(task: TaskCreate, background_tasks: BackgroundTasks, db: Session = Depends(deps.get_db)):
    db_request = crud_request.create_request(db, task)
    background_tasks.add_task(call_celery_task, db_request.id)
    return {"status": "Task has been submitted to be processed in the background"}

@router.post('/submit_multiple_tasks/', response_model=list[dict])
async def submit_multiple_tasks(tasks: MultipleTasksCreate, background_tasks: BackgroundTasks, db: Session = Depends(deps.get_db)):
    db_requests = []
    for task in tasks.tasks:
        db_request = crud_request.create_request(db, task)
        background_tasks.add_task(call_celery_task, db_request.id)
        db_requests.append({"status": "Task has been submitted to be processed in the background"})
    return db_requests

@router.get('/tasks/', response_model=list[Request])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    tasks = crud_request.get_requests(db, skip=skip, limit=limit)
    return tasks

@router.get('/task_status/{task_id}', response_model=dict)
def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    return {"task_id": task_id, "status": task_result.status, "result": task_result.result}
