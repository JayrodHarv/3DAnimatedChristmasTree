from fastapi import APIRouter
from controller import controller

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

@api_router.post("/play/{name}")
def play(name: str):
    controller.play(name)
    return controller.status()

@api_router.post("/pause")
def pause():
    controller.pause()
    return controller.status()

@api_router.post("/resume")
def resume():
    controller.resume()
    return controller.status()

@api_router.post("/speed/{value}")
def speed(value: float):
    controller.set_speed(value)
    return controller.status()
