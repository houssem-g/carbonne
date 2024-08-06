
from sqlalchemy.orm import Session
from app.models.request import Request
from app.schemas.request import RequestCreate


def create_request(db: Session, request: RequestCreate):
    db_request = Request(a=request.a, b=request.b)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def get_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Request).offset(skip).limit(limit).all()
