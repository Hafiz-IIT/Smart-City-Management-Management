from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from App.API.incidents import router as incidents_router
from App.API.predict import router as predict_router
from App.API.stream import router as stream_router

app = FastAPI(title="Smart City Twin")
app.include_router(incidents_router)
app.include_router(predict_router)
app.include_router(stream_router)

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "Templates"))


@app.get("/")
def dashboard(req: Request):
    return templates.TemplateResponse("index.html", {"request": req})


@app.get("/incidents")
def incidents(req: Request):
    return templates.TemplateResponse("incidents.html", {"request": req})


@app.get("/admin")
def admin(req: Request):
    return templates.TemplateResponse("admin.html", {"request": req})
