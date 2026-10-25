import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from services.produto_service import ProdutoService
from schemas.produto import ProdutoCreate

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def mock_categoria_service():
    return MagicMock()

@pytest.fixture
def mock_fornecedor_service():
    return MagicMock()

@pytest.fixture
def produto_service(mock_repo, mock_categoria_service, mock_fornecedor_service):
    return ProdutoService(mock_repo, mock_categoria_service, mock_fornecedor_service)

# 1. Teste de Sucesso na Criação
def test_criar_produto_sucesso(produto_service, mock_repo, mock_categoria_service, mock_fornecedor_service):
    # Simula que o código está disponível (não existe no banco)
    mock_repo.get_by_codigo.return_value = None
    mock_repo.create.return_value = MagicMock(id=1, codigo="PROD123")

    produto_data = ProdutoCreate(
        nome="Notebook",
        codigo="PROD123",
        preco_custo=1000.0,
        preco_venda=1500.0,
        categoria_id=1,
        fornecedor_id=1,
        quantidade_em_estoque=0,  
        estoque_minimo=5          
    )

    resultado = produto_service.criar_produto(produto_data)

    # Garante que os serviços de validação de dependência foram consultados
    mock_categoria_service.obter_categoria.assert_called_once_with(1)
    mock_fornecedor_service.obter_fornecedor.assert_called_once_with(1)
    
    assert resultado.codigo == "PROD123"

# 2. Teste de Bloqueio por Código Duplicado
def test_criar_produto_codigo_duplicado_deve_falhar(produto_service, mock_repo, mock_categoria_service, mock_fornecedor_service):
    # Simula que o repositório já encontrou um produto com esse código
    mock_repo.get_by_codigo.return_value = MagicMock(id=2, codigo="PROD123")

    produto_data = ProdutoCreate(
        nome="Notebook",
        codigo="PROD123",
        preco_custo=1000.0,
        preco_venda=1500.0,
        categoria_id=1,
        fornecedor_id=1,
        quantidade_em_estoque=0,  
        estoque_minimo=5          
    )

    with pytest.raises(HTTPException) as exc_info:
        produto_service.criar_produto(produto_data)

    assert exc_info.value.status_code == 400
    assert "já existe produto cadastrado com este código" in exc_info.value.detail.lower()

# 3. Teste de Bloqueio por Preço de Venda Menor que Custo
def test_criar_produto_preco_invalido_deve_falhar(produto_service, mock_repo, mock_categoria_service, mock_fornecedor_service):
    mock_repo.get_by_codigo.return_value = None

    # Preço de venda intencionalmente menor que o custo
    produto_data = ProdutoCreate(
        nome="Notebook",
        codigo="PROD123",
        preco_custo=2000.0, #Custo maior
        preco_venda=1500.0, #Venda menor
        categoria_id=1,
        fornecedor_id=1,
        quantidade_em_estoque=0,  
        estoque_minimo=5          
    )

    with pytest.raises(HTTPException) as exc_info:
        produto_service.criar_produto(produto_data)

    assert exc_info.value.status_code == 400
    assert "menor que o custo" in exc_info.value.detail.lower()