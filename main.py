from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from routers import todos

# Create database tables
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="ToDo API",
    description="A simple ToDo API with full CRUD operations, powered by FastAPI and SQLAlchemy.",
    version="1.0.0"
)

app.include_router(todos.router, prefix="/todos")

# -------------------- Dependency --------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- API Endpoints --------------------
@app.get("/todos", response_model=list[schemas.Todo])
def read_todos(db: Session = Depends(get_db)):
    return crud.get_todos(db)

@app.post("/todos", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)

@app.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    return crud.update_todo(db, todo_id, todo)

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    return crud.delete_todo(db, todo_id)

@app.get("/todos/search", response_model=list[schemas.Todo])
def search_todos(q: str | None, db: Session = Depends(get_db)):
    return crud.search_todos(db, q)


# -------------------- Static Files --------------------
# static files must be in the end of main(after api endpoints)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")