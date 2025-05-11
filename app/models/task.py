from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(Date)
    priority = Column(String)  # low, medium, high
    status = Column(String, default="pending")  # pending, done
    tag = Column(String)  # учёба, дом и т.д.