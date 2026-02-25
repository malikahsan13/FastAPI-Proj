from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from database import get_db
from sqlalchemy.orm import Session
from models import ToDO
from typing import List

router = APIRouter()


class TodoCreate(BaseModel):
    id: int
    title: str
    description: str
    done: bool


class ToDoResponse(TodoCreate):
    id: int


todos = []


@router.get('/', response_model=List[ToDoResponse])
def show_Todos(db: Session = Depends(get_db)):
    return db.query(ToDO).all()


@router.post('/', response_model=ToDoResponse)
def create_Todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = ToDO(title=todo.title,
                    description=todo.description, done=todo.done)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)  # it will fetch ids sometime it gives id empty
    return new_todo


@router.put('/{todo_id}', response_model=ToDoResponse)
def update_Todo(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = db.query(ToDO).filter(ToDO.id == todo_id).first()
    if not todo:
        return HTTPException(status_code=404, detail="Todo Not Found")
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.done = todo.done
    db.commit()  # why session not added check
    return todo


@router.delete("/{todo_id}")
def delete_Todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(ToDO).filter(ToDO.id == todo_id).first()
    if not db_todo:
        return HTTPException(status_code=404, detail="Todo Not Found")
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo Deleted Successfully"}
