from fastapi import APIRouter, HTTPException, Path, Query
from starlette import status
from ..models import User, Task
from ..dependencies import *
from ..schemas import *


router=APIRouter(
    prefix="/admin",
    tags=["admin"]
)


# users
@router.get("/users", status_code=status.HTTP_200_OK)
async def read_all_users(db: db_dependency, user: user_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    return db.query(User).all()


@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(db: db_dependency, user: user_dependency,
                         user_id: int= Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    user_model=db.query(User).filter(User.id==user_id).first()
    
    if user_model is None:
        raise HTTPException(status_code=404, detail="The user not found")
    
    return user_model


@router.post("/create-user", status_code=status.HTTP_201_CREATED)
async def create_user(user: user_dependency, db: db_dependency,
                      user_request: UserRequest):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    user_model = User(**user_request.model_dump())

    db.add(user_model)
    db.commit()

 
@router.put("/users/update_user/{user_id}", status_code=status.HTTP_200_OK)
async def update_user_info(user_update: UserUpdate,db: db_dependency,
                           user: user_dependency, user_id: int=Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    user_model = db.query(User).filter(User.id == user_id).first()
    
    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.username is not None:
        user_model.username = user_update.username
    if user_update.email is not None:
        user_model.email = user_update.email
    if user_update.role is not None:
        user_model.role = user_update.role
        
    if user_update.password and user_update.new_password:
        if not bcrypt_context.verify(user_update.password, user_model.hashed_password):
            raise HTTPException(status_code=401, detail="Current password incorrect")
        user_model.hashed_password = bcrypt_context.hash(user_update.new_password)

    db.commit()
    db.refresh(user_model)
    return user_model


@router.delete("/users/delete-user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user: user_dependency, db: db_dependency,
                            user_id: int=Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')

    user_model=db.query(User).filter(User.id==user_id).first()
    
    if user_model is None:
        raise HTTPException(status_code=404, detail="The user not found")
    db.query(User).filter(User.id==user_id).delete()
    db.commit()
    

# tasks
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_tasks(db: db_dependency, user: user_dependency):
    if user is None or user.get("user_role") not in ["user", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return db.query(Task).all()


@router.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_by_id(db: db_dependency, user: user_dependency,
                         task_id: int= Path(gt=0)):
    if user is None or user.get("user_role") not in ["user", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    task_model=db.query(Task).filter(Task.id==task_id).first()
    
    if task_model is None:
        raise HTTPException(status_code=404, detail="The task not found")
    return task_model


    
@router.put("/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_task(user: user_dependency, db: db_dependency,
                      task_request: TaskUpdate,
                      task_id: int = Path(gt=0)):
    if user is None or user.get("user_role") not in ["user", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    task_model = db.query(Task).filter(Task.id == task_id).first()
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
    if user is None or user.get("user_role") not in ["user", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    task_model = db.query(Task).filter(Task.id == task_id).first()
    if task_model is None:
        raise HTTPException(status_code=404, detail='Task not found.')
    db.query(Task).filter(Task.id == task_id).delete()

    db.commit()