from fastapi import Depends
from sqlalchemy.orm import Session
from config.db import Session 
from repositories.produto_repository import ProdutoRepository
from services.produto_service import ProdutoService

# Injeta a sessão do banco de dados na requisição
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

# Injeta o Repository e o Service encadeados
def get_produto_service(db: Session = Depends(get_db)) -> ProdutoService:
    repo = ProdutoRepository(db)
    return ProdutoService(repo)