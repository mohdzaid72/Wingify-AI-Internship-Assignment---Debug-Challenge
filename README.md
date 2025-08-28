# Wingify-AI-Internship-Assignment---Debug-Challenge

# 📊 Financial Document Analyzer

A scalable backend system for analyzing financial PDFs using **FastAPI**, **Celery**, **CrewAI**, and **SQLAlchemy**.  
It allows users to upload documents, queue analysis tasks, and retrieve **investment insights** powered by LLM agents.

---

## 🐞 Bugs & Fixes

| Bug | Description | Fix |
|-----|-------------|-----|
| `422 Validation Error` | File or query missing in `/analyze` | Enforced `multipart/form-data` validation for `file` & `query` |
| `500 Internal Server Error` | Celery result malformed or missing fields | Used safe `.get()` unpacking and `TaskResult` Pydantic model |
| `MySQL CompileError` | MySQL requires `VARCHAR(length)` | Defined explicit lengths for `String` columns in `models.py` |
| Swagger UI mismatch | Response showed `null` fields | Split models: `AnalysisQueueResponse` (`/analyze`) & `TaskResult` (`/results/{task_id}`) |

---

## ⚙️ Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-username/financial-document-analyzer.git
cd financial-document-analyzer
```

### 2. Configure Environment
Create a `.env` file:
```env
DATABASE_URL=mysql+pymysql://user:password@localhost/dbname
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start Services
```bash
# Start Redis
redis-server

# Start Celery Worker
celery -A worker worker --loglevel=info --concurrency=4

# Start FastAPI Server
uvicorn main:app --reload
```

---

## 📡 Usage

### Upload & Analyze a Document
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

## 📚 API Endpoints

### `GET /`
Health check:
```json
{ "message": "Financial Document Analyzer API is running" }
```

### `POST /analyze`
Queue a document for analysis.

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
Fetch analysis result.

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
- **SQLAlchemy + MySQL** → Persistent storage  
- **Swagger UI** → Interactive API testing  

---
