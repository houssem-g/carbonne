from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.request import Base 
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
