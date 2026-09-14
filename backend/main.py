"""FastAPI application entrypoint for Deni."""
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import __version__

app = FastAPI(title="Deni", version=__version__)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@app.get("/health")
def health() -> dict:
    """Liveness check."""
    return {"status": "ok", "service": "deni", "version": __version__}


# Serve the SPA. Mounted last so API routes take precedence.
if FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")


@app.get("/")
def index() -> FileResponse:
    """Serve the app shell."""
    return FileResponse(str(FRONTEND_DIR / "index.html"))
