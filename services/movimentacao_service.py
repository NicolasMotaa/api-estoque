from fastapi import HTTPException, status
from repositories.movimentacao_repository import MovimentacaoRepository
from schemas.movimentacao import MovimentacaoCreate
from services.produto_service import ProdutoService
from services.fornecedor_service import FornecedorService
from models.movimentacao import Tipo

class MovimentacaoService():

    def __init__(self, repo: MovimentacaoRepository, produto_service:ProdutoService, fornecedor_service: FornecedorService):
        self.repo = repo
        self.produto_service = produto_service
        self.fornecedor_service = fornecedor_service
        

    def obter_movimentacao(self, movimentacao_id: int):
        movimentacao = self.repo.get_by_id(movimentacao_id)

        if not movimentacao:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Movimentação não encontrada")
        return movimentacao

    def registrar_movimentacao(self, movimentacao_data: MovimentacaoCreate):
        #função do produto_service verifica se o produto informado existe
        mov_produto = self.produto_service.obter_produto(movimentacao_data.produto_id)
        if movimentacao_data.tipo == Tipo.ENTRADA:
            mov_produto.quantidade_em_estoque += movimentacao_data.quantidade
        elif movimentacao_data.tipo == Tipo.SAIDA: 
            if movimentacao_data.quantidade > mov_produto.quantidade_em_estoque:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Pedido de movimentação excedeu a quantidade em estoque do produto.")
            
            mov_produto.quantidade_em_estoque -= movimentacao_data.quantidade

        return self.repo.create(movimentacao_data)

    def get_all(self):
        return self.repo.get_all()

    def listar_por_produto(self, produto_id: int):
        # Valida se o produto existe 
        self.produto_service.obter_produto(produto_id)
        return self.repo.get_by_produto(produto_id)

    def listar_por_fornecedor(self, fornecedor_id: int):
        # Valida se o fornecedor existe 
        self.fornecedor_service.obter_fornecedor(fornecedor_id)        
        return self.repo.get_by_fornecedor(fornecedor_id)

    def listar_por_periodo(self, data_inicio, data_fim):
        if data_inicio > data_fim:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A data de início não pode ser maior que a data de fim."
            )
        return self.repo.get_by_periodo(data_inicio, data_fim)
