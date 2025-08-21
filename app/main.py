from fastapi import FastAPI, HTTPException, Depends, Request, Response, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
app = FastAPI()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def todo_query(db: Session):
    return db.query(models.Todo)

@app.post("/todos/", response_model=schemas.Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.TodoCreate, request: Request, response: Response, db: Session = Depends(get_db)):
    db_todo = models.Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    response.headers["Location"] = str(request.url_for("read_todo", todo_id=db_todo.id))
    return db_todo

@app.get("/todos/", response_model=list[schemas.Todo])
def read_todos(db: Session = Depends(get_db)):
    return todo_query(db).all()

@app.get("/todos/{todo_id}", response_model=schemas.Todo, name="read_todo")
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

@app.get("/users/{user_id}", response_model=schemas.User, name="read_user")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, request: Request, response: Response, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter_by(email=user.email).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    response.headers["Location"] = str(request.url_for("read_user", user_id=new_user.id))
    return new_user