from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
import models, schemas

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def todo_query(db: Session):
    return db.query(models.Todo)

@app.post("/todos/", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_todo = models.Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos/", response_model=list[schemas.Todo])
def read_todos(db: Session = Depends(get_db)):
    return todo_query(db).all()

@app.get("/todos/{todo_id}", response_model=schemas.Todo)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = todo_query(db).get(todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo

@app.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, update: schemas.TodoUpdate, db: Session = Depends(get_db)):
    todo = todo_query(db).get(todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.title = update.title or todo.title
    todo.completed = update.completed if update.completed is not None else todo.completed
    db.commit()

    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = todo_query(db).get(todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()

    return {"message": "Deleted successfully"}