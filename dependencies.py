from fastapi import Depends
from sqlalchemy.orm import Session
from config.db import Session 
from repositories.produto_repository import ProdutoRepository
from services.produto_service import ProdutoService
from repositories.fornecedor_repository import FornecedorRepository
from services.fornecedor_service import FornecedorService
from repositories.categoria_repository import CategoriaRepository
from services.categoria_service import CategoriaService
from repositories.movimentacao_repository import MovimentacaoRepository
from services.movimentacao_service import MovimentacaoService

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

def get_fornecedor_service(db: Session = Depends(get_db)) -> FornecedorService:
    repo = FornecedorRepository(db)
    return FornecedorService(repo)

def get_categoria_service(db: Session = Depends(get_db)) -> CategoriaService:
    repo = CategoriaRepository(db)
    return CategoriaService(repo)

def get_movimentacao_service(db: Session = Depends(get_db)):
    repo = MovimentacaoRepository(db)
    
    produto_repo = ProdutoRepository(db)
    produto_service = ProdutoService(produto_repo)
    
    fornecedor_repo = FornecedorRepository(db)
    fornecedor_service = FornecedorService(fornecedor_repo)
    
    return MovimentacaoService(repo, produto_service, fornecedor_service)