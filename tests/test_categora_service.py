import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from services.categoria_service import CategoriaService
from schemas.categoria import CategoriaCreate

# 1. Preparação (Fixture)
@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def categoria_service(mock_repo):
    return CategoriaService(mock_repo)

# 2. Testando o caminho feliz (Sucesso)
def test_criar_categoria_sucesso(categoria_service, mock_repo):
    # Configura o mock: o banco diz que não existe categoria com esse nome
    mock_repo.get_by_nome.return_value = None 
    # Configura o mock do retorno do create
    mock_repo.create.return_value = MagicMock(id=1, nome="Eletrônicos")

    categoria_data = CategoriaCreate(nome="Eletrônicos")
    resultado = categoria_service.criar_categoria(categoria_data)

    assert resultado.nome == "Eletrônicos"
    mock_repo.create.assert_called_once() # Garante que a função de salvar no banco foi chamada

# 3. Testando as barreiras de erro (Exceptions)
def test_criar_categoria_nome_em_branco_deve_falhar(categoria_service):
    categoria_data = CategoriaCreate(nome="   ")
    
    # O pytest captura a exceção para podermos validar o status code
    with pytest.raises(HTTPException) as exc_info:
        categoria_service.criar_categoria(categoria_data)
        
    assert exc_info.value.status_code == 400
    assert "não pode ser vazio" in exc_info.value.detail