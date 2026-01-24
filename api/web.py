from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

web_router = APIRouter()

# Project root = parent of api/
BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = BASE_DIR / "web"

# Serve /web/* → filesystem web/*
web_router.mount(
    "/web",
    StaticFiles(directory=str(WEB_DIR)),
    name="web"
)

@web_router.get("/")
def index():
    return FileResponse(WEB_DIR / "index.html")
