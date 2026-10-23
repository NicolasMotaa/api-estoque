from fastapi import FastAPI
from models.categoria import Categoria #temporário para o sqlalchemy ler a entidade antes de add router próprio
from routes.produto_route import router as produto_router
from routes.fornecedor_route import router as fornecedor_router
app = FastAPI (title= "API de gerenciamento de estoque")

app.include_router(produto_router)
app.include_router(fornecedor_router)




