from fastapi import APIRouter, Depends, status
from dependencies import get_categoria_service
from schemas.categoria import CategoriaCreate, CategoriaResponse, CategoriaUpdate
from services.categoria_service import CategoriaService

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def criar_categoria(
    categoria_in: CategoriaCreate,
    service: CategoriaService = Depends(get_categoria_service)
):
    return service.criar_categoria(categoria_in)

@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias(service: CategoriaService = Depends(get_categoria_service)):
    return service.listar_categorias()

@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obter_categoria(
    categoria_id: int,
    service: CategoriaService = Depends(get_categoria_service)
):
    return service.obter_categoria(categoria_id)

@router.put("/{categoria_id}", response_model=CategoriaResponse)
def atualizar_categoria(
    categoria_id: int,
    categoria_in: CategoriaUpdate,
    service: CategoriaService = Depends(get_categoria_service)
):
    return service.atualizar_categoria(categoria_id, categoria_in)

@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_categoria(
    categoria_id: int,
    service: CategoriaService = Depends(get_categoria_service)
):
    service.excluir_categoria(categoria_id)

# Funcionalidade Avançada
@router.get("/{categoria_id}/produtos", response_model=list[CategoriaResponse])
def listar_produtos_da_categoria(
    categoria_id: int,
    service: CategoriaService = Depends(get_categoria_service)
):
    return service.obter_produtos_da_categoria(categoria_id)