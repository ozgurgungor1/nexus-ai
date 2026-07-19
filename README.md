# NEXUS AI

NEXUS AI is a modular and extensible AI platform built with FastAPI, SQLite, AI provider adapters, and agent-oriented request handling.

## Features

- JWT authentication with role support
- Chat endpoint with agent routing (assistant, coder, researcher, planner)
- OpenAI / Ollama / local model provider support
- Conversation and message persistence using SQLAlchemy + SQLite
- File upload and extraction for PDF, Word, Excel, TXT, CSV, JSON
- Settings, memory, and history APIs
- CORS support and OpenAPI docs

## Requirements

- Python 3.11+
- SQLite

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Create a `.env` file in the repository root with:

```env
DATABASE_URL=sqlite:///./data/nexus_ai.db
SECRET_KEY=replace-with-strong-secret
OPENAI_API_KEY=your_openai_api_key
OLLAMA_URL=http://localhost:11434
LOCAL_MODEL_API_URL=
```

4. Run the application:

```bash
python -m uvicorn backend.main:app --reload
```

5. Open Swagger UI at `http://127.0.0.1:8000/docs`

## Docker

Build and run with Docker Compose:

```bash
docker compose up --build
```

## Project Structure

- `backend/` - FastAPI backend implementation
- `backend/llm/` - AI provider adapters
- `backend/agents/` - task-specific agents
- `backend/database/` - SQLAlchemy models and session
- `backend/services/` - business logic and domain services
- `backend/api/` - REST API routes
- `backend/middleware/` - authentication middleware
- `backend/utils/` - logging and helpers

## Testing

Run tests from the repository root:

```bash
pytest
```
