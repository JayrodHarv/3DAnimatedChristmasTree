from fastapi import APIRouter
from controller import controller

router = APIRouter(prefix="/api")

@router.get("/status")
def status():
    return controller.status()

@router.get("/animations")
def animations():
    return controller.list_animations()

@router.post("/next")
def next_anim():
    controller.next()
    return controller.status()

@router.post("/play/{name}")
def play(name: str):
    controller.play(name)
    return controller.status()

@router.post("/pause")
def pause():
    controller.pause()
    return controller.status()

@router.post("/resume")
def resume():
    controller.resume()
    return controller.status()

@router.post("/speed/{value}")
def speed(value: float):
    controller.set_speed(value)
    return controller.status()
