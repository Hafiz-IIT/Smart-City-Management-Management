# app/main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.incidents import router as incidents_router
from app.api.predict import router as predict_router
from app.api.stream import router as stream_router

app = FastAPI(title="Smart City Twin", default_response_class=None)

app.include_router(incidents_router)
app.include_router(predict_router)
app.include_router(stream_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def dashboard(req: Request):
    return templates.TemplateResponse("index.html", {"request": req})

@app.get("/incidents")
def incidents(req: Request):
    return templates.TemplateResponse("incidents.html", {"request": req})

@app.get("/admin")
def admin(req: Request):
    return templates.TemplateResponse("admin.html", {"request": req})
