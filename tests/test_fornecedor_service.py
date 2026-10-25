import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from services.fornecedor_service import FornecedorService
from schemas.fornecedor import FornecedorCreate

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def fornecedor_service(mock_repo):
    return FornecedorService(mock_repo)

# 1. Teste de Sucesso na Exclusão
def test_excluir_fornecedor_sucesso(fornecedor_service, mock_repo):
    # Simula que o fornecedor existe no banco
    mock_repo.get_by_id.return_value = MagicMock(id=1, nome="Fornecedor Teste")
    
    # Simula que a lista de produtos vinculados está vazia (permitindo a exclusão)
    mock_repo.get_produtos_do_fornecedor.return_value = []

    fornecedor_service.excluir_fornecedor(1)

    # Garante que a função de deletar do repositório foi chamada
    mock_repo.delete.assert_called_once()

# 2. Teste de Bloqueio por Produtos Vinculados
def test_excluir_fornecedor_com_produtos_deve_falhar(fornecedor_service, mock_repo):
    mock_repo.get_by_id.return_value = MagicMock(id=1, nome="Fornecedor Teste")
    
    # Simula que o repositório encontrou produtos vinculados
    mock_repo.get_produtos_do_fornecedor.return_value = [MagicMock(id=99)]

    with pytest.raises(HTTPException) as exc_info:
        fornecedor_service.excluir_fornecedor(1)

    # Verifica se a API barrou no lugar certo
    assert exc_info.value.status_code == 400
    assert "Existem produtos associados" in exc_info.value.detail