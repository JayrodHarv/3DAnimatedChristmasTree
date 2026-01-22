from fastapi import FastAPI
from controller import controller
from api.web import router as web_router

app = FastAPI()

app.include_router(web_router)

@app.get("/api/status")
def status():
    return controller.status()

@app.get("/api/animations")
def animations():
    return controller.list_animations()

@app.post("/api/next")
def next_anim():
    controller.next()
    return controller.status()

@app.post("/api/play/{name}")
def play(name: str):
    controller.play(name)
    return controller.status()

@app.post("/api/pause")
def pause():
    controller.pause()
    return controller.status()

@app.post("/api/resume")
def resume():
    controller.resume()
    return controller.status()

@app.post("/api/speed/{value}")
def speed(value: float):
    controller.set_speed(value)
    return controller.status()
