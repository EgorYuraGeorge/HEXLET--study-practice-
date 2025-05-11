from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .task import Base

DATABASE_URL = "postgresql+psycopg2://hexlet:12345@localhost:5432/task_manager"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)