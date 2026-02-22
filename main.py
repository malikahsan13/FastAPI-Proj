from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def home():
    return {"msg": "hello world"}


@app.post('/')
def home():
    return {"msg": "hi world"}


@app.put('/')
def home():
    return {"msg": "hi world"}
