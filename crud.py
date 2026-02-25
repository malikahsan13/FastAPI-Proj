from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from database import get_db
from sqlalchemy.orm import Session
from models import ToDO
from typing import List

router = APIRouter()

class TodoCreate(BaseModel):
    id: int
    name: str
    description: str
    done: bool

class ToDoResponse(TodoCreate):
    id: int

todos = []


@router.get('/')
def show_Todos():
    return todos


@router.post('/', response_model=ToDoResponse)
def create_Todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = ToDO(title=todo.name, description=todo.description, done=todo.done)
    db.add(new_todo)
    db.commit()
    return new_todo


@router.put('/{todo_id}')
def update_Todo(todo_id: int, updated_todo: TodoCreate):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[i] = updated_todo
            return {"msg": "Todo updated successfully"}
    return {"msg": "Failed to update Todo"}


@router.delete("/{todo_id}")
def delete_Todo(todo_id: int):
    global todos
    todos = [todo for todo in todos if todo.id != todo_id]
    return {"msg": "Todo Deleted successfully"}
