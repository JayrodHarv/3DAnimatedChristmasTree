import threading
from scheduler import run_scheduler
from controller import controller, pixels, coords

from fastapi import FastAPI
from api.control_api import router as api_router
from api.web import router as web_router

app = FastAPI()

app.include_router(api_router)
app.include_router(web_router)

# Start scheduler
threading.Thread(
    target=run_scheduler,
    args=(pixels, coords, controller),
    daemon=True
).start()

# For debugging: list all routes
for r in app.routes:
    print(r.path, r.methods)

# Start API
import uvicorn

uvicorn.run(web_router, host="0.0.0.0", port=8000)
