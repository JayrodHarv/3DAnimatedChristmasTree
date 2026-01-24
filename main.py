import threading
from scheduler import run_scheduler, stop_scheduler
from controller import controller, pixels, coords
from pathlib import Path
from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI
from api.control_api import api_router
from api.web import web_router

app = FastAPI()

# Project root = parent of api/
BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = BASE_DIR / "web"

# Serve /web/* → filesystem web/*
web_router.mount(
    "/web",
    StaticFiles(directory=str(WEB_DIR)),
    name="web"
)

app.include_router(api_router, prefix="/api")
app.include_router(web_router)

# Start scheduler
scheduler_thread = threading.Thread(
    target=run_scheduler,
    args=(pixels, coords, controller),
    daemon=True
)
scheduler_thread.start()

@app.on_event("shutdown")
def shutdown():
    print("Shutting down scheduler... clearing pixels")

    stop_scheduler()

    # Clear pixels on shutdown
    pixels.fill((0, 0, 0))
    pixels.show()