from fastapi import APIRouter
from controller import controller

router = APIRouter(prefix="/api")

@router.get("/api/status")
def status():
    return controller.status()

@router.get("/api/animations")
def animations():
    return controller.list_animations()

@router.post("/api/next")
def next_anim():
    controller.next()
    return controller.status()

@router.post("/api/play/{name}")
def play(name: str):
    controller.play(name)
    return controller.status()

@router.post("/api/pause")
def pause():
    controller.pause()
    return controller.status()

@router.post("/api/resume")
def resume():
    controller.resume()
    return controller.status()

@router.post("/api/speed/{value}")
def speed(value: float):
    controller.set_speed(value)
    return controller.status()
