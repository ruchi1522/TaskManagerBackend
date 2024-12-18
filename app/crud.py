from sqlalchemy.orm import Session
from app import models, schema

def get_tasks(db: Session, skip: int = 0, limit: int = 10): return db.query(models.Task).offset(skip).limit(limit).all()

def create_task(db: Session, task: schema.TaskCreate):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        deadline=task.deadline,
        is_completed=task.is_completed
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: schema.TaskCreate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db_task.title = task.title
        db_task.description = task.description
        db_task.deadline = task.deadline
        db_task.is_completed = task.is_completed
        db.commit()
        db.refresh(db_task)
        return db_task
    else:
        return None