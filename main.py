from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def home():
    return {"msg": "hello world"}


@app.post('/')
def hello():
    return {"msg": "hi world"}
