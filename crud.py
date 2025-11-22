from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime

def get_todos(db: Session):
    return db.query(models.Todo).all()

def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: int, todo: schemas.TodoUpdate):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not db_todo:
        raise Exception("Todo not found")
    db_todo.completed = todo.completed
    db_todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not db_todo:
        raise Exception("Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"detail": "Todo deleted"}

def search_todos(db: Session, q: str):
    return db.query(models.Todo).filter(models.Todo.title.contains(q)).all()
