from datetime import timedelta
from app.core.celery_app import celery_app
from sqlalchemy.orm import sessionmaker
from app.core.config import engine
from app.models.request import TaskResult
import redis
import os
from app.core.logging_config import logger 


REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
redis_client = redis.StrictRedis.from_url(REDIS_URL)


@celery_app.task(bind=True, name="app.tasks.periodic_tasks.move_results")
def move_results(self):
    logger.info("Running move_results task")
    session = SessionLocal()
    try:
        for key in redis_client.scan_iter("celery-task-meta-*"):
            logger.info(f"Processing key: {key}")
            task_result = redis_client.get(key)
            if task_result:
                task_data = self.app.backend.decode_result(task_result)
                task_id = key.decode("utf-8").replace("celery-task-meta-", "")
                
                if task_data["result"] is None:
                    continue
                new_task_result = TaskResult(
                    task_id=task_id,
                    status=task_data['status'],
                    result=str(task_data['result'])
                )
                
                session.add(new_task_result)
                session.commit()
                
                logger.info(f"Moved result for task {task_id} to SQL DB")

                redis_client.delete(key)
    except Exception as e:
        logger.error(f"Error moving results: {e}")
        session.rollback()
    finally:
        session.close()


celery_app.conf.beat_schedule = {
    'move-results-every-30-seconds': {
        'task': 'app.tasks.periodic_tasks.move_results',
        'schedule': timedelta(seconds=30),  # For testing purposes I used 30 seconds usually it should be adjusted based on the number of call made to celery tasks
    },
}
