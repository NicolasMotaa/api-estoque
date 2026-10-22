from fastapi import FastAPI
from routes.produto_route import router as produto_router
app = FastAPI (title= "API de gerenciamento de estoque")

app.include_router(produto_router)



