from sqlalchemy.orm import Session
from models.categoria import Categoria
from models.produto import Produto
from schemas.categoria import CategoriaCreate

class CategoriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, categoria_data: CategoriaCreate) -> Categoria:
        nova_categoria = Categoria(**categoria_data.model_dump())
        self.db.add(nova_categoria)
        self.db.commit()
        self.db.refresh(nova_categoria)
        return nova_categoria

    def get_all(self) -> list[Categoria]:
        return self.db.query(Categoria).all()

    def get_by_id(self, categoria_id: int) -> Categoria | None:
        return self.db.query(Categoria).filter(Categoria.id == categoria_id).first()

    #Para validação de unicidade
    def get_by_nome(self, nome: str) -> Categoria | None:
        return self.db.query(Categoria).filter(Categoria.nome == nome).first()

    def update(self, db_categoria: Categoria, update_data: dict) -> Categoria:
        for key, value in update_data.items():
            setattr(db_categoria, key, value)
        
        self.db.commit()
        self.db.refresh(db_categoria)
        return db_categoria

    def delete(self, db_categoria: Categoria) -> None:
        self.db.delete(db_categoria)
        self.db.commit()

    #Consulta Avançada 
    def get_produtos_da_categoria(self, categoria_id: int) -> list[Produto]:
        return self.db.query(Produto).filter(Produto.categoria_id == categoria_id).all()