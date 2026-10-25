import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from services.movimentacao_service import MovimentacaoService
from schemas.movimentacao import MovimentacaoCreate
from models.movimentacao import Tipo

# 1. Preparação (Fixtures)
@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def mock_produto_service():
    return MagicMock()

@pytest.fixture
def mock_fornecedor_service():
    return MagicMock()

@pytest.fixture
def movimentacao_service(mock_repo, mock_produto_service, mock_fornecedor_service):
    return MovimentacaoService(mock_repo, mock_produto_service, mock_fornecedor_service)

# 2. Teste: Entrada de Estoque
def test_registrar_entrada_sucesso(movimentacao_service, mock_produto_service, mock_repo):
    # Simulamos um produto com 10 unidades no estoque
    mock_produto = MagicMock(id=1, quantidade_em_estoque=10)
    mock_produto_service.obter_produto.return_value = mock_produto
    
    # Configuramos o retorno do repositório
    mock_repo.create.return_value = MagicMock(id=1, tipo=Tipo.ENTRADA, quantidade=5)

    mov_data = MovimentacaoCreate(produto_id=1, tipo=Tipo.ENTRADA, quantidade=5)
    movimentacao_service.registrar_movimentacao(mov_data)

    # Verifica se a matemática foi aplicada corretamente no objeto em memória
    assert mock_produto.quantidade_em_estoque == 15
    mock_repo.create.assert_called_once_with(mov_data)

# 3. Teste: Saída de Estoque (Sucesso)
def test_registrar_saida_sucesso(movimentacao_service, mock_produto_service, mock_repo):
    # Simulamos um produto com 10 unidades
    mock_produto = MagicMock(id=1, quantidade_em_estoque=10)
    mock_produto_service.obter_produto.return_value = mock_produto

    mov_data = MovimentacaoCreate(produto_id=1, tipo=Tipo.SAIDA, quantidade=3)
    movimentacao_service.registrar_movimentacao(mov_data)

    # 10 - 3 = 7
    assert mock_produto.quantidade_em_estoque == 7
    mock_repo.create.assert_called_once_with(mov_data)

# 4. Teste: Saída Bloqueada por Estoque Insuficiente
def test_registrar_saida_estoque_insuficiente_deve_falhar(movimentacao_service, mock_produto_service):
    # Simulamos um produto com apenas 2 unidades
    mock_produto = MagicMock(id=1, quantidade_em_estoque=2)
    mock_produto_service.obter_produto.return_value = mock_produto

    # Tentamos tirar 5
    mov_data = MovimentacaoCreate(produto_id=1, tipo=Tipo.SAIDA, quantidade=5)

    with pytest.raises(HTTPException) as exc_info:
        movimentacao_service.registrar_movimentacao(mov_data)

    # Verifica se a API bloqueou com o status correto
    assert exc_info.value.status_code == 400
    assert "excedeu a quantidade em estoque" in exc_info.value.detail