from sqlalchemy import Column, String, DateTime, Integer, Text
from .database import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    password_hash = Column(String)
    email = Column(String, nullable=True)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    content = Column(Text)

class Solution(Base):
    __tablename__ = "solutions"

    id = Column(String, primary_key=True, index=True)
    team_id = Column(String, index=True)
    task_id = Column(String, index=True)
    answer = Column(Text)
    status = Column(String)
    timestamp = Column(DateTime)