from sqlalchemy.orm import Session
from models.movimentacao import Movimentacao
from schemas.movimentacao import MovimentacaoCreate
from models.produto import Produto
from datetime import datetime

#O repositório de Movimentações não deve contar com funções de Update ou Delete pois estas são registros imutáveis

class MovimentacaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, movimentacao_id: int) -> Movimentacao | None:
        return self.db.query(Movimentacao).filter(Movimentacao.id == movimentacao_id).first()

    def get_all(self) -> list[Movimentacao]:
        return self.db.query(Movimentacao).all()

    def create(self, movimentacao_data: MovimentacaoCreate) -> Movimentacao | None:
        db_movimentacao = Movimentacao(**movimentacao_data.model_dump())
        self.db.add(db_movimentacao)
        self.db.commit()
        self.db.refresh(db_movimentacao)
        return db_movimentacao

    #Funcionalidades avançadas

    def get_by_produto(self, produto_id: int) -> list[Movimentacao]:
        return self.db.query(Movimentacao).filter(Movimentacao.produto_id == produto_id).all()

    def get_by_fornecedor(self, fornecedor_id: int) -> list[Movimentacao]:
        # Faz um JOIN automático entre Movimentacao e Produto para poder filtrar pela coluna do fornecedor
        return self.db.query(Movimentacao).join(Produto).filter(Produto.fornecedor_id == fornecedor_id).all()

    def get_by_periodo(self, data_inicio: datetime, data_fim: datetime) -> list[Movimentacao]:
        return self.db.query(Movimentacao).filter(
            Movimentacao.data >= data_inicio,
            Movimentacao.data <= data_fim
        ).all()