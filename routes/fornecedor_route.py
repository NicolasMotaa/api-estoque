from fastapi import APIRouter, Depends, status
from schemas.fornecedor import FornecedorCreate, FornecedorResponse, FornecedorUpdate
from schemas.produto import ProdutoResponse 
from services.fornecedor_service import FornecedorService
from dependencies import get_fornecedor_service

router = APIRouter(prefix="/fornecedores", tags=["Fornecedores"])

@router.post("/", response_model=FornecedorResponse, status_code=status.HTTP_201_CREATED)
def criar_fornecedor(
    fornecedor_in: FornecedorCreate,
    service: FornecedorService = Depends(get_fornecedor_service)
):
    return service.criar_fornecedor(fornecedor_in)

@router.get("/", response_model=list[FornecedorResponse])
def listar_fornecedores(service: FornecedorService = Depends(get_fornecedor_service)):
    return service.listar_fornecedores()

@router.get("/{fornecedor_id}", response_model=FornecedorResponse)
def obter_fornecedor(
    fornecedor_id: int, 
    service: FornecedorService = Depends(get_fornecedor_service)
):
    return service.obter_fornecedor(fornecedor_id)

@router.put("/{fornecedor_id}", response_model=FornecedorResponse)
def atualizar_fornecedor(
    fornecedor_id: int, 
    fornecedor_in: FornecedorUpdate, 
    service: FornecedorService = Depends(get_fornecedor_service)
):
    return service.atualizar_fornecedor(fornecedor_id, fornecedor_in)

@router.delete("/{fornecedor_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_fornecedor(
    fornecedor_id: int, 
    service: FornecedorService = Depends(get_fornecedor_service)
):
    service.excluir_fornecedor(fornecedor_id)

# Funcionalidade Avançada 
@router.get("/{fornecedor_id}/produtos", response_model=list[ProdutoResponse])
def listar_produtos_do_fornecedor(
    fornecedor_id: int, 
    service: FornecedorService = Depends(get_fornecedor_service)
):
    return service.get_list_of_produtos(fornecedor_id)