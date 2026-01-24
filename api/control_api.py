from fastapi import APIRouter
from controller import controller, safe_shutdown, pixels
from pydantic import BaseModel

api_router = APIRouter()

@api_router.get("/status")
def status():
    return controller.status()

@api_router.get("/animations")
def animations():
    return controller.list_animations()

@api_router.post("/next")
def next_anim():
    controller.next()
    return controller.status()

@api_router.post("/previous")
def previous_anim():
    controller.previous()
    return controller.status()

@api_router.post("/play/{name}")
def play(name: str):
    controller.play(name)
    return controller.status()

@api_router.post("/toggle")
def toggle():
    controller.toggle()
    return controller.status()

@api_router.post("/speed/{value}")
def speed(value: float):
    controller.set_speed(value)
    return controller.status()

class ShuffleRequest(BaseModel):
    duration: float  # seconds per animation

@api_router.post("/shuffle")
def shuffle_animations(req: ShuffleRequest):
    controller.start_shuffle(duration=req.duration)
    return {
        "status": "ok",
        "mode": "shuffle",
        "duration": req.duration
    }

@api_router.post("/shutdown")
def shutdown_pi():
    safe_shutdown(pixels)
    return {"status": "shutting down"}
