from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .database import engine, Base
from .routers import users, tasks, admin, api
from .dependencies import user_dependency_cookie

app = FastAPI()

Base.metadata.create_all(bind=engine)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"
STATIC_DIR = BASE_DIR / "frontend" / "static"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request, user: user_dependency_cookie):
    if not user:
        return templates.TemplateResponse("index.html", {"request": request, "username": None})
    return templates.TemplateResponse("index.html", {"request": request, "username": user.get("username")})

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(admin.router)
app.include_router(api.router)