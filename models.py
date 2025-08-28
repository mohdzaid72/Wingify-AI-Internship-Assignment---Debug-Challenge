from pydantic import BaseModel
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class AnalysisTask(Base):
    __tablename__ = "analysis_tasks"

    task_id = Column(String(64), primary_key=True)
    file_name = Column(String(255))
    file_id = Column(String(64))
    query = Column(Text)
    result = Column(Text)
    status = Column(String(32))
    created_at = Column(DateTime, default=datetime.utcnow)

class AnalysisQueueResponse(BaseModel):
    status: str
    task_id: str
    file_processed: str

class TaskResult(BaseModel):
    status: str
    task_id: str
    file: str | None = None
    file_id: str | None = None
    query: str | None = None
    result: str | None = None
    error: str | None = None
