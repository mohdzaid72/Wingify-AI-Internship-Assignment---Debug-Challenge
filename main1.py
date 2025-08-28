from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Path
import os, uuid, aiofiles, logging
from worker import run_analysis_task
from celery.result import AsyncResult
from models import AnalysisQueueResponse, TaskResult
from db import engine
from models import AnalysisTask

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize DB tables
AnalysisTask.metadata.create_all(bind=engine)

app = FastAPI(title="Financial Document Analyzer", version="0.1.0")

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze", response_model=AnalysisQueueResponse)
async def analyze_financial_document_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"

    try:
        os.makedirs("data", exist_ok=True)
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)

        query = query.strip() or "Analyze this financial document for investment insights"
        task = run_analysis_task.delay(query, file_path, file.filename, file_id)

        return {
            "status": "queued",
            "task_id": task.id,
            "file_processed": file.filename
        }

    except Exception as e:
        logger.error("Error queuing analysis task", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/results/{task_id}", response_model=TaskResult)
def get_task_result(task_id: str = Path(...)):
    result = AsyncResult(task_id)

    if result.state == "PENDING":
        return TaskResult(status="pending", task_id=task_id)

    elif result.state == "SUCCESS":
        data = result.result
        if isinstance(data, dict):
            return TaskResult(
                status=data.get("status", "completed"),
                task_id=data.get("task_id", task_id),
                file=data.get("file"),
                file_id=data.get("file_id"),
                query=data.get("query"),
                result=data.get("result"),
                error=data.get("error")
            )
        else:
            return TaskResult(status="error", task_id=task_id, error="Invalid result format")

    else:
        return TaskResult(status=result.state, task_id=task_id, error="Task failed or unknown state")
