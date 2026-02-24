from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter()


class Todo(BaseModel):
    id: int
    name: str
    description: str


todos = []


@router.get('/')
def show_Todos():
    return todos


@router.post('/')
def create_Todo(todo: Todo):
    todos.append(todo)
    return {"msg": "Todo created successfully"}


@router.put('/{todo_id}')
def update_Todo(todo_id: int, updated_todo: Todo):
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
