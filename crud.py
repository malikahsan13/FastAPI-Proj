from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from database import get_db
from sqlalchemy.orm import Session
from models import ToDO
from typing import List
#  if want to run for normal html css
from fastapi import Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

router = APIRouter()

#  if want to run for normal html css
templates = Jinja2Templates(directory="templates")

class TodoCreate(BaseModel):
    title: str
    description: str
    done: bool


class ToDoResponse(TodoCreate):
    id: int


todos = []


@router.get("/", response_model=List[ToDoResponse])
def show_Todos(request: Request, db:Session=Depends(get_db)):
    todos = db.query(ToDO).all()
    return templates.TemplateResponse('todo_list.html', {"request":request, "todos": todos})

# @router.get("/", response_model=List[ToDoResponse])
# def show_Todos(db:Session=Depends(get_db)):
#     return db.query(ToDO).all()
    
@router.post("/",response_model=ToDoResponse)
def create_Todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = ToDO(title=todo.title, description=todo.description, done=todo.done)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@router.put("/{todo_id}", response_model=ToDoResponse)
def update_todo(todo_id: int, todo: TodoCreate, db : Session=Depends(get_db)):
    db_todo = db.query(ToDO).filter(ToDO.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.done = todo.done
    db.commit()
    return db_todo

@router.delete("/{todo_id}")
def delete_todo(todo_id:int, db: Session = Depends(get_db)):
    db_todo = db.query(ToDO).filter(ToDO.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    db.delete(db_todo)
    db.commit()
    return {"Todo Deleted Successfully"}
