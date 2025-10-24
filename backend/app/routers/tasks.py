from fastapi import APIRouter, status, Path, Form
from fastapi.responses import HTMLResponse
from ..dependencies import *
from ..models import Task


router=APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, user: user_dependency_cookie, db: db_dependency):
    if not user:
        return RedirectResponse("/users/login-page", status_code=302)

    tasks = db.query(Task).filter(Task.user_id == user.get("id")).all()
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "tasks": tasks, "username": user.get("username")})


@router.get("/create", response_class=HTMLResponse)
async def create_task_page(request: Request, user: user_dependency_cookie):
    if not user:
        return redirect_to_login()
    return templates.TemplateResponse(
        "create_task.html",
        {"request": request, "username": user.get("username")}
    )


@router.post("/create", response_class=HTMLResponse)
async def create_task(request: Request,db: db_dependency,
                      user: user_dependency_cookie,title: str = Form(...),
                      description: str = Form(""),status_: str = Form("todo"),
                      start_time: str = Form(None),end_time: str = Form(None),):
    if not user:
        return redirect_to_login()

    def parse_dt(dt_str):
        if dt_str:
            return datetime.fromisoformat(dt_str)
        return None

    now_dt = datetime.now(timezone.utc)
    if status_ == "in_progress" and not start_time:
        start_time = now_dt.isoformat()
    if status_ == "done":
        if not start_time:
            start_time = now_dt.isoformat()
        end_time = now_dt.isoformat()

    new_task = Task(
        title=title,
        description=description,
        status=status_,
        user_id=user.get("id"),
        start_time=parse_dt(start_time),
        end_time=parse_dt(end_time)
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return RedirectResponse(url="/tasks/", status_code=302)


@router.get("/{task_id}", response_class=HTMLResponse)
async def task_detail(db: db_dependency, user: user_dependency_cookie, 
                      request: Request, task_id: int = Path(gt=0)):
    if not user:
        return redirect_to_login()

    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.get("id")).first()
    if not task:
        return templates.TemplateResponse("error.html",
                                          {"request": request, "message": "Task not found"},
                                          status_code=404)
    return templates.TemplateResponse("task_detail.html",
                                      {"request": request, "task": task, "username": user.get("username"), "now": datetime.now()})


@router.get("/{task_id}/edit", response_class=HTMLResponse)
async def edit_task_page(db: db_dependency, user: user_dependency_cookie,
                         request: Request, task_id: int = Path(gt=0)):
    if not user:
        return redirect_to_login()

    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.get("id")).first()
    if not task:
        return templates.TemplateResponse("error.html",
                                          {"request": request, "message": "Task not found"},
                                          status_code=404)
    return templates.TemplateResponse("edit_task.html",
                                      {"request": request, "task": task, "username": user.get("username")})


@router.post("/{task_id}/edit", response_class=HTMLResponse)
async def update_task(db: db_dependency, user: user_dependency_cookie,
                      request: Request, task_id: int = Path(gt=0),
                      title: str = Form(...),description: str = Form(""),
                      status_: str = Form("todo"),start_time: str = Form(None),
                      end_time: str = Form(None)):
    if not user:
        return redirect_to_login()

    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.get("id")).first()
    if not task:
        return templates.TemplateResponse("error.html",
                                          {"request": request, "message": "Task not found"},
                                          status_code=404)

    def parse_dt(dt_str):
        if dt_str:
            return datetime.fromisoformat(dt_str)
        return None

    now_dt = datetime.now(timezone.utc)
    if status_ == "in_progress" and not start_time:
        start_time = now_dt.isoformat()
    if status_ == "done":
        if not start_time:
            start_time = task.start_time.isoformat() if task.start_time else now_dt.isoformat()
        end_time = now_dt.isoformat()
    if status_ == "todo":
        start_time = None
        end_time = None

    task.title = title
    task.description = description
    task.status = status_
    task.start_time = parse_dt(start_time)
    task.end_time = parse_dt(end_time)

    db.commit()
    db.refresh(task)

    return RedirectResponse(url=f"/tasks/{task_id}", status_code=302)


@router.post("/{task_id}/mark-done", response_class=HTMLResponse)
async def mark_task_done(db: db_dependency, user: user_dependency_cookie, 
                         task_id: int = Path(gt=0)):
    if not user:
        return redirect_to_login()

    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.get("id")).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    now_dt = datetime.now(timezone.utc)
    if task.status != "done":
        task.status = "done"
        if not task.start_time:
            task.start_time = now_dt
        task.end_time = now_dt

    db.commit()
    db.refresh(task)
    return RedirectResponse(url="/tasks/", status_code=302)


@router.post("/{task_id}/delete", response_class=HTMLResponse)
async def delete_task(db: db_dependency,user: user_dependency_cookie,
                      task_id: int = Path(gt=0)):
    if not user:
        return redirect_to_login()

    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.get("id")).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return RedirectResponse(url="/tasks/", status_code=302)