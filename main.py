import threading
from utils import runtime
from animations import ANIMATIONS
from controller import AnimationController
from scheduler import run_scheduler

COORDS_FILE = "tree_d_coords.txt"

# Load hardware + data
coords, pixels = runtime.setup_tree(
    coords_file=COORDS_FILE
)

animations = ANIMATIONS

controller = AnimationController(animations)

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
