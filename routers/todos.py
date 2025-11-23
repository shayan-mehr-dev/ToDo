from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import Todo, TodoCreate
import crud

router = APIRouter(
    prefix="/todos",
    tags=["Todos"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=Todo, status_code=status.HTTP_201_CREATED, summary="Create a new todo", description="Create a todo item by providing a title and description.")
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)

@router.get("/", response_model=List[Todo], summary="Get all todos", description="Retrieve a list of all todos.")
def get_todos(db: Session = Depends(get_db)):
    return crud.get_todos(db)

@router.get("/{todo_id}", response_model=Todo, summary="Get a todo by ID", description="Retrieve a single todo by its ID.")
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.delete("/{todo_id}", status_code=status.HTTP_200_OK, summary="Delete a todo", description="Delete a todo by its ID.")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    success = crud.delete_todo(db, todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"detail": f"Todo {todo_id} deleted successfully"}

@router.get("/search", response_model=list[Todo])
def search_todos(q: str | None, db: Session = Depends(get_db)):
    return crud.search_todos(db, q)