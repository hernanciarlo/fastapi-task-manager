from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.models.task import Task as TaskModel
from app.models.user import User
from app.core.auth_utils import get_current_user, get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "/",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskModel:
    db_task = TaskModel(title=task.title, owner_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get(
    "/",
    response_model=List[TaskOut],
)
def read_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[TaskModel]:
    return db.query(TaskModel).filter(TaskModel.owner_id == current_user.id).all()


@router.get(
    "/{task_id}",
    response_model=TaskOut,
)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskModel:
    db_task = (
        db.query(TaskModel)
        .filter(
            TaskModel.id == task_id,
            TaskModel.owner_id == current_user.id,
        )
        .first()
    )
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada",
        )
    return db_task


@router.patch(
    "/{task_id}",
    response_model=TaskOut,
)
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskModel:
    db_task = (
        db.query(TaskModel)
        .filter(
            TaskModel.id == task_id,
            TaskModel.owner_id == current_user.id,
        )
        .first()
    )
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada",
        )
    if task.title is not None:
        db_task.title = task.title
    if task.done is not None:
        db_task.done = task.done
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    db_task = (
        db.query(TaskModel)
        .filter(
            TaskModel.id == task_id,
            TaskModel.owner_id == current_user.id,
        )
        .first()
    )
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada",
        )
    db.delete(db_task)
    db.commit()
    return None
