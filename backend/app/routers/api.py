from fastapi import APIRouter, Path
from ..models import Task, User
from ..dependencies import *
from ..schemas import TaskCreate, TaskUpdate

router=APIRouter(
    prefix="/api",
    tags=["api"]
)


# apis that are accessable to users
@router.get("/api/users/me", status_code=status.HTTP_200_OK)
async def get_current_user_info(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    user_model = db.query(User).filter(User.id == user.get('id')).first()
    return user_model


# tasks
@router.get("/tasks", status_code=status.HTTP_200_OK)
async def api_get_tasks(user: user_dependency, db: db_dependency):
    return db.query(Task).filter(Task.user_id == user.get("id")).all()


@router.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_by_id(db: db_dependency, user: user_dependency,
                         task_id: int= Path(gt=0)):
    if not user:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    task_model=db.query(Task).filter(Task.id==task_id)\
        .filter(Task.user_id == user.get('id')).first()
    
    if task_model is None:
        raise HTTPException(status_code=404, detail="The task not found")
    return task_model


@router.post("/create-task", status_code=status.HTTP_201_CREATED)
async def create_task(user: user_dependency, db: db_dependency,
                      task_request: TaskCreate):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    task_model = Task(**task_request.model_dump(), user_id=user.get('id'))

    db.add(task_model)
    db.commit()
    
    
@router.put("/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_task(user: user_dependency, db: db_dependency,
                      task_request: TaskUpdate,
                      task_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    task_model = db.query(Task).filter(Task.id == task_id)\
        .filter(Task.user_id == user.get('id')).first()
    if task_model is None:
        raise HTTPException(status_code=404, detail='Task not found.')

    task_model.title = task_request.title
    task_model.description = task_request.description
    task_model.status = task_request.status
    task_model.start_time = task_request.start_time
    task_model.end_time=task_request.end_time

    db.add(task_model)
    db.commit()


@router.delete("/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(user: user_dependency, db: db_dependency, task_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    task_model = db.query(Task).filter(Task.id == task_id)\
        .filter(Task.user_id == user.get('id')).first()
    if task_model is None:
        raise HTTPException(status_code=404, detail='Task not found.')
    db.query(Task).filter(Task.id == task_id).filter(Task.user_id == user.get('id')).delete()

    db.commit()