from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, timezone

def now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String(50), default="user")

    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="todo")
    start_time = Column(DateTime, default=now, nullable=True)
    end_time = Column(DateTime, default=now, nullable=True)

    owner = relationship("User", back_populates="tasks")