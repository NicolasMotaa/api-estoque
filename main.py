from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from config.logger import logger
from routes.produto_route import router as produto_router
from routes.fornecedor_route import router as fornecedor_router
from routes.categoria_route import router as categoria_router
from routes.movimentacao_route import router as movimentacao_router

app = FastAPI (title= "API de gerenciamento de estoque")

# Captura de Erros do Banco de Dados
#Evita expôr dados sensíveis do BD em casos de erros 500 relacionados.
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Falha no BD ao acessar {request.url.path}: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Erro interno de processamento de dados. Contate o suporte."}
    )

#Captura de Qualquer Outro Erro Inesperado
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    logger.error(f"Erro Crítico não tratado em {request.url.path}: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Ocorreu um erro inesperado no servidor."}
    )


#Rotas
app.include_router(produto_router)
app.include_router(fornecedor_router)
app.include_router(categoria_router)
app.include_router(movimentacao_router)





