# Wingify-AI-Internship-Assignment---Debug-Challenge

# 📊 Financial Document Analyzer

A scalable backend system built with **FastAPI**, **Celery**, **CrewAI**, and **SQLAlchemy**, designed to analyze financial documents using open-source LLMs. Users can upload PDFs, queue analysis tasks, and retrieve investment insights asynchronously.

## Queue Worker Model and DataBase are integrated

---

## 🐞 Bugs Found & Fixes

### ✅ FastAPI & Celery Integration
| Bug | Fix |
|-----|-----|
| `422 Validation Error` on `/analyze` | Ensured `multipart/form-data` and validated `file` and `query` inputs |
| `500 Internal Server Error` on `/results/{task_id}` | Safely unpacked Celery result using `.get()` and wrapped in `TaskResult` |
| MySQL `VARCHAR requires a length` | Added explicit lengths to all `String` columns in `models.py` |
| Swagger UI mismatch | Split response models: `AnalysisQueueResponse` for `/analyze`, `TaskResult` for `/results/{task_id}` |
| Celery result expired too quickly | Set `result_expires = 3600` in Celery config |
| Missing table creation | Added `AnalysisTask.metadata.create_all(bind=engine)` in `main1.py` |
| File not saved or removed properly | Used `aiofiles` for async saving and wrapped `os.remove()` in try-except |
| Task not returning expected format | Standardized return dictionary in `worker.py` |
| No task routing logic | Implemented `select_task(query)` to dynamically choose CrewAI task |

### ✅ CrewAI & Tooling
| Bug | Fix |
|-----|-----|
| CrewAI input mapping bug | Added `input_schema` to define `"query"` and `"file_path"` |
| Synchronous file I/O in async endpoint | Replaced `open()` with `aiofiles` |
| Missing file type validation | Added `.endswith(".pdf")` check |
| CrewAI file access race condition | Moved file deletion into Celery worker after processing |
| No OCR fallback for scanned PDFs | Added `pytesseract` fallback for image-based pages |
| Blocking CrewAI execution in FastAPI | Offloaded `run_crew()` to Celery via `delay()` |
| No result persistence | Stored results in MySQL using SQLAlchemy |
| Hardcoded PostgreSQL driver | Switched to MySQL and updated `db.py` and `frequirments.txt` |
| Unstructured logging | Replaced `print()` with `logger.error(..., exc_info=True)` |

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/financial-document-analyzer.git
cd financial-document-analyzer
```

### 2. Create a `.env` File
```env
DATABASE_URL=mysql+pymysql://user:password@localhost/dbname
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
```

### 3. Install Dependencies
```bash
pip install -r frequirments.txt
```

### 4. Start Services
```bash
# Start Redis
redis-server

# Start Celery Worker
celery -A worker worker --loglevel=info --concurrency=4

# Start FastAPI Server
uvicorn main1:app --reload
```

---

## 📡 Usage Instructions

### Upload & Analyze a Financial Document
```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -F "file=@TSLA-Q2-2025-Update.pdf" \
  -F "query=Analyze this financial document for investment insights"
```

### Retrieve Analysis Result
```bash
curl -X GET http://127.0.0.1:8000/results/{task_id}
```

---

## 📚 API Documentation

### `GET /`
Health check:
```json
{ "message": "Financial Document Analyzer API is running" }
```

### `POST /analyze`
Queue a financial document for analysis.

**Request (multipart/form-data):**
- `file`: PDF file *(required)*
- `query`: Investment-related question *(optional)*

**Response:**
```json
{
  "status": "queued",
  "task_id": "uuid",
  "file_processed": "TSLA-Q2-2025-Update.pdf"
}
```

### `GET /results/{task_id}`
Fetch the result of a completed analysis.

**Response:**
```json
{
  "status": "completed",
  "task_id": "uuid",
  "file": "TSLA-Q2-2025-Update.pdf",
  "file_id": "uuid",
  "query": "Analyze this financial document",
  "result": "Detailed investment insights...",
  "error": null
}
```

---

## 🧠 Architecture Highlights
- **FastAPI** → Async API request handling  
- **Celery + Redis** → Background task execution  
- **CrewAI** → LLM-powered financial analysis  
- **SQLAlchemy + MySQL** → Persistent task storage  
- **Swagger UI** → Interactive API testing  
