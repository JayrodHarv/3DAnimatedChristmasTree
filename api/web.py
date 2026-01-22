from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")

router.mount("/web", StaticFiles(directory=WEB_DIR), name="web")

@router.get("/")
def index():
    return FileResponse(os.path.join(WEB_DIR, "index.html"))
