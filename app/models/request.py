from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True, index=True)
    a = Column(Integer)
    b = Column(Integer)
    result = Column(Integer, default=None)
    status = Column(String, default='pending')


class TaskResult(Base):
    __tablename__ = "task_results"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    status = Column(String)
    result = Column(Text)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
