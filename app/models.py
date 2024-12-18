from app.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    deadline = Column(TIMESTAMP(timezone=True), nullable=False)
    is_completed = Column(Boolean, server_default='FALSE')
