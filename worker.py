import os
import logging
from celery import Celery
from dotenv import load_dotenv
from crewai import Crew, Process
from agents import financial_analyst
from task import (
    analyze_financial_document,
    investment_analysis,
    risk_assessment,
    verification
)
from db import SessionLocal
from models import AnalysisTask

load_dotenv()
logger = logging.getLogger(__name__)

celery_app = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

def select_task(query: str):
    query_lower = query.lower()
    if "risk" in query_lower:
        return risk_assessment
    elif "verify" in query_lower or "check" in query_lower:
        return verification
    elif "invest" in query_lower or "buy" in query_lower:
        return investment_analysis
    else:
        return analyze_financial_document

@celery_app.task(name="run_analysis_task")
def run_analysis_task(query: str, file_path: str, filename: str, file_id: str):
    try:
        selected_task = select_task(query)
        crew = Crew(
            agents=[financial_analyst],
            tasks=[selected_task],
            process=Process.sequential
        )

        result = crew.kickoff(inputs={"query": query, "file_path": file_path})

        db = SessionLocal()
        db_task = AnalysisTask(
            task_id=run_analysis_task.request.id,
            file_name=filename,
            file_id=file_id,
            query=query,
            result=str(result),
            status="completed"
        )
        db.add(db_task)
        db.commit()
        db.close()

        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

        return {
            "status": "completed",
            "task_id": run_analysis_task.request.id,
            "file": filename,
            "file_id": file_id,
            "query": query,
            "result": str(result),
            "error": None
        }

    except Exception as e:
        logger.error(f"Task {file_id} failed: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "task_id": run_analysis_task.request.id,
            "file": filename,
            "file_id": file_id,
            "query": query,
            "result": None,
            "error": str(e)
        }
