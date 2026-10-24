from fastapi import APIRouter, Depends, status, Query
from datetime import datetime
from schemas.movimentacao import MovimentacaoCreate, MovimentacaoResponse
from services.movimentacao_service import MovimentacaoService
from dependencies import get_movimentacao_service

router = APIRouter(prefix="/movimentacoes", tags=["Movimentações"])

@router.post("/", response_model=MovimentacaoResponse, status_code=status.HTTP_201_CREATED)
def registrar_movimentacao(
    movimentacao_in: MovimentacaoCreate,
    service: MovimentacaoService = Depends(get_movimentacao_service)
):
    return service.registrar_movimentacao(movimentacao_in)

@router.get("/", response_model=list[MovimentacaoResponse])
def listar_movimentacoes(service: MovimentacaoService = Depends(get_movimentacao_service)):
    return service.get_all()

@router.get("/{movimentacao_id}", response_model=MovimentacaoResponse)
def obter_movimentacao(
    movimentacao_id: int,
    service: MovimentacaoService = Depends(get_movimentacao_service)
):
    return service.obter_movimentacao(movimentacao_id)

# Consultas Avançadas

@router.get("/produto/{produto_id}", response_model=list[MovimentacaoResponse])
def listar_por_produto(
    produto_id: int,
    service: MovimentacaoService = Depends(get_movimentacao_service)
):
    return service.listar_por_produto(produto_id)

@router.get("/fornecedor/{fornecedor_id}", response_model=list[MovimentacaoResponse])
def listar_por_fornecedor(
    fornecedor_id: int,
    service: MovimentacaoService = Depends(get_movimentacao_service)
):
    return service.listar_por_fornecedor(fornecedor_id)

#uso de Query Parameters evita erros de rota. 
#rota será acessada no formato de query string
@router.get("/relatorios/periodo", response_model=list[MovimentacaoResponse])
def listar_por_periodo(
    data_inicio: datetime = Query(..., description="Data inicial no formato YYYY-MM-DDTHH:MM:SS"),
    data_fim: datetime = Query(..., description="Data final no formato YYYY-MM-DDTHH:MM:SS"),
    service: MovimentacaoService = Depends(get_movimentacao_service)
):
    return service.listar_por_periodo(data_inicio, data_fim)