from fastapi import FastAPI
from config.db import Session
from models.produto import Produto

app = FastAPI ()

@app.get("/produto")
def get_produto():
    return {"Hello":"Produto"}

