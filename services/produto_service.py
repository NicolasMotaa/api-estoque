from repositories.produto_repository import ProdutoRepository
from schemas.produto import ProdutoCreate, ProdutoUpdate
from fastapi import HTTPException, status
from services.categoria_service import CategoriaService
from services.fornecedor_service import FornecedorService
from config.logger import logger

class ProdutoService:
    def __init__(self, repo: ProdutoRepository, categoria_service: CategoriaService, fornecedor_service: FornecedorService):
        self.repo = repo
        self.categoria_service = categoria_service
        self.fornecedor_service = fornecedor_service

    def criar_produto(self, produto_data: ProdutoCreate):

        #verificações de existência de categoria e fornecedor. 
        self.categoria_service.obter_categoria(produto_data.categoria_id)
        self.fornecedor_service.obter_fornecedor(produto_data.fornecedor_id)

        #regra: código deve ser único
        if self.repo.get_by_codigo(produto_data.codigo):

            logger.warning(
                f"Tentativa de criação de Produto bloqueada:"
                f"Código {produto_data.codigo} já está em uso"
                )

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="já existe produto cadastrado com este código")

        #regra: o preco de venda deve ser maior que o preço de custo
        if produto_data.preco_venda <  produto_data.preco_custo:

            logger.warning(
                f"Tentativa de criação de Produto bloqueada:"
                f"(Preço de venda solicitado: {produto_data.preco_venda}, Preco de custo solicitado: {produto_data.preco_custo})"
                )

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="O valor de venda não pode ser menor que o custo do produto")

        novo_produto = self.repo.create(produto_data)
        
        logger.info(
                    f"Produto criado: ID do Produto: {novo_produto.id}"
                )

        return novo_produto

    def listar_produtos(self):
        return self.repo.get_all()

    def obter_produto(self, produto_id: int):
        produto = self.repo.get_by_id(produto_id)
        if not produto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Produto não encontrado")

        return produto

    def buscar_estoque_baixo(self):
        return self.repo.get_estoque_baixo()
    
    def atualizar_produto(self, produto_id: int, produto_data: ProdutoUpdate):
        #utiliza a função do próprio service. Em caso de erro, a exceção é lançada nela mesma.
        db_produto = self.obter_produto(produto_id)

        #verifica o caso de tentar mudar o código para um já existente
        if produto_data.codigo and produto_data.codigo != db_produto.codigo:
            if self.repo.get_by_codigo(produto_data.codigo):

                logger.warning(
                    f"Tentativa de atualização bloqueada: Código já existente "
                    f"(Código solicitado: {produto_data.codigo})"
                    )
                
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                    detail="Código já cadastrado em outro produto.")

        #ignora os Nones
        update_data = produto_data.model_dump(exclude_unset=True)

        produto_atualizado = self.repo.update(db_produto, update_data)
        
        logger.info(
            f"Produto atualizado: ID do Produto: {produto_atualizado.id}"
            )

        return produto_atualizado

    def excluir_produto(self, produto_id: int):
        # Busca para ver se existe (lança 404 se não existir)
        db_produto = self.obter_produto(produto_id)
        
        # O repositório faz a exclusão
        self.repo.delete(db_produto)
        logger.info(f"Produto excluído: Produto ID {produto_id}")