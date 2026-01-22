import threading
from scheduler import run_scheduler
from controller import controller

# Start scheduler
threading.Thread(
    target=run_scheduler,
    args=(pixels, coords, controller),
    daemon=True
).start()

# Start API
import uvicorn
from api.control_api import app

uvicorn.run(app, host="0.0.0.0", port=8000)
