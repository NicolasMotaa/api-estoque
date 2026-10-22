from sqlalchemy.orm import Session
from models.produto import Produto
from schemas.produto import ProdutoCreate

class ProdutoRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id (self, produto_id: int) -> Produto | None:
        return self.db.query(Produto).filter(Produto.id == produto_id).first()

    def get_by_codigo(self, codigo: int) -> Produto | None:
        return self.db.query(Produto).filter(Produto.codigo == codigo).first()

    ##consulta avançada
    def get_estoque_baixo(self) -> list[Produto]:
        return self.db.query(Produto).filter(Produto.quantidade_em_estoque <= Produto.estoque_minimo).all()

    def create(self, produto_data: ProdutoCreate) -> Produto:
        db_produto = Produto(**produto_data.model_dump())
        self.db.add(db_produto)
        self.db.commit()
        self.db.refresh(db_produto)
        return db_produto