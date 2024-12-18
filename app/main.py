import sys
from typing import List
sys.path.append('D:\\Ruchi\\Projects\\Backend\\.venv\\Lib\\site-packages')

from fastapi import Depends, FastAPI, HTTPException
from app import models, database, schema, crud  
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:4200"],  
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks/", response_model=schema.Task)  
def create_task(task: schema.TaskCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_task(db=db, task=task)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=f"Error creating task: {str(e)}")
    
@app.get("/tasks/", response_model=List[schema.Task])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks

@app.put("/tasks/{task_id}", response_model=schema.Task)
def update_task(
    task_id: int,
    task: schema.TaskCreate,
    db: Session = Depends(get_db)
):
    db_task = crud.get_tasks(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return crud.update_task(db=db, task_id=task_id, task=task)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
