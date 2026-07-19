from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from backend.core.config import settings
from backend.database.database import Base, engine
from backend.routes import router
from backend.utils.logger import logger

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="NEXUS AI is a modular, extensible AI platform built with FastAPI and SQLite.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent / "static"), name="static")

app.include_router(router)


@app.on_event("startup")
def on_startup() -> None:
    logger.info("Starting NEXUS AI application")
    Base.metadata.create_all(bind=engine)


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    index_file = Path(__file__).resolve().parent / "static" / "index.html"
    return index_file.read_text(encoding="utf-8")
