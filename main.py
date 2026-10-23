from fastapi import FastAPI
from routes.produto_route import router as produto_router
from routes.fornecedor_route import router as fornecedor_router
from routes.categoria_route import router as categoria_router

app = FastAPI (title= "API de gerenciamento de estoque")

app.include_router(produto_router)
app.include_router(fornecedor_router)
app.include_router(categoria_router)




