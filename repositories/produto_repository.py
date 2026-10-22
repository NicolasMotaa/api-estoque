from sqlalchemy.orm import Session
from models.produto import Produto
from schemas.produto import ProdutoCreate, ProdutoUpdate

class ProdutoRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id (self, produto_id: int) -> Produto | None:
        return self.db.query(Produto).filter(Produto.id == produto_id).first()

    def get_by_codigo(self, codigo: int) -> Produto | None:
        return self.db.query(Produto).filter(Produto.codigo == codigo).first()

    def get_all(self) -> list[Produto]:
        return self.db.query(Produto).all()
       
    ##consulta avançada
    def get_estoque_baixo(self) -> list[Produto]:
        return self.db.query(Produto).filter(Produto.quantidade_em_estoque <= Produto.estoque_minimo).all()

    def create(self, produto_data: ProdutoCreate) -> Produto:
        #converte o DTO em dicionário
        db_produto = Produto(**produto_data.model_dump())
        #adiciona o objeto à sessão do db
        self.db.add(db_produto)
        #executa a transação (adiciona de fato no bd)
        self.db.commit()
        #atualiza na memória
        self.db.refresh(db_produto)
        return db_produto

    def update(self, db_produto: Produto, update_data: ProdutoUpdate) -> Produto:
        for key, value in update_data.items():
            setattr(db_produto, key, value)

        self.db.commit()
        self.db.refresh(db_produto)
        return db_produto
        

    def delete(self, db_produto: Produto) -> None:
        self.db.delete(db_produto)
        self.db.commit()