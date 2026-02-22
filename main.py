from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Todo(BaseModel):
    id: int
    name: str
    description: str


todos = []


@app.get('/')
def show_Todos():
    return todos


@app.post('/')
def create_Todo(todo: Todo):
    todos.append(todo)
    return {"msg": "Todo created successfully"}


@app.put('/')
def home():
    return {"msg": "hi world"}
