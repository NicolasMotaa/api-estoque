from fastapi import APIRouter, Depends, status
from schemas.produto import ProdutoCreate, ProdutoResponse, ProdutoUpdate
from services.produto_service import ProdutoService
from dependencies import get_produto_service

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(
    produto_in: ProdutoCreate,
    service: ProdutoService = Depends(get_produto_service)
):
    return service.criar_produto(produto_in)

@router.get("/estoque-baixo", response_model=list[ProdutoResponse])
def listar_estoque_baixo(service: ProdutoService = Depends(get_produto_service)):
    return service.buscar_estoque_baixo()

@router.get("/", response_model=list[ProdutoResponse])
def listar_produtos(service: ProdutoService = Depends(get_produto_service)):
    return service.listar_produtos()

@router.get("/{produto_id}", response_model=ProdutoResponse)
def obter_produto(produto_id: int, service: ProdutoService = Depends(get_produto_service)):
    return service.obter_produto(produto_id)

@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int, 
    produto_in: ProdutoUpdate, 
    service: ProdutoService = Depends(get_produto_service)
):
    return service.atualizar_produto(produto_id, produto_in)

@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_produto(produto_id: int, service: ProdutoService = Depends(get_produto_service)):
    service.excluir_produto(produto_id)