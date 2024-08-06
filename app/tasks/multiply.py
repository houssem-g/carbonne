from app.core.celery_app import celery_app
from sqlalchemy.orm import sessionmaker
from app.core.config import engine
from app.models.request import Request
import time
from app.core.logging_config import logger


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@celery_app.task(bind=True, default_retry_delay=300, max_retries=3, soft_time_limit=600, time_limit=660)
def multiply(self, request_id: int):
    session = SessionLocal()
    result = None
    try:
        request = session.query(Request).filter(Request.id == request_id).first()
        if request:
            logger.info(f"Task {self.request.id} started for request_id={request_id} with a={request.a}, b={request.b}")
            result = request.a * request.b
            time.sleep(5)
            request.result = result
            request.status = 'completed'
            session.commit()
            logger.info(f"Task {self.request.id} completed for request_id={request_id}, result={result}")
        else:
            logger.error(f"Request not found for request_id={request_id}")
    except Exception as e:
        logger.error(f"Error in task {self.request.id} for request_id={request_id}: {e}")
        session.rollback()
        raise self.retry(exc=e)
    finally:
        session.close()
    return result