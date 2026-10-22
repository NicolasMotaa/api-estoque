from sqlalchemy.orm import Session
from models.fornecedor import Fornecedor
from schemas.fornecedor import FornecedorCreate, FornecedorUpdate
from models.produto import Produto


class FornecedorRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, fornecedor_id: int) -> Fornecedor | None:
        return self.db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()

    #para verificação de integridade (email único)
    def get_by_email(self, fornecedor_email: str) -> Fornecedor | None:
        return self.db.query(Fornecedor).filter(Fornecedor.email == fornecedor_email).first()

    def get_all(self) -> list[Fornecedor]:
            return self.db.query(Fornecedor).all()

    #para verificação de integridade (cnpj único)
    def get_by_cnpj(self, fornecedor_cnpj: str) -> Fornecedor | None:
        return self.db.query(Fornecedor).filter(Fornecedor.cnpj == fornecedor_cnpj).first()


    def get_produtos_do_fornecedor(self, fornecedor_id: int) -> list[Produto]:
        return self.db.query(Produto).filter(Produto.fornecedor_id == fornecedor_id).all()

    def create(self, fornecedor_data: FornecedorCreate) -> Fornecedor:

         db_fornecedor = Fornecedor(**fornecedor_data.model_dump())
         self.db.add(db_fornecedor)
         self.db.commit()
         self.db.refresh(db_fornecedor)
         return db_fornecedor

    def update(self, db_fornecedor: Fornecedor, update_data: FornecedorUpdate) -> Fornecedor:
        for key, value in update_data.items():
            setattr(db_fornecedor, key, value)
         
        self.db.commit()
        self.db.refresh(db_fornecedor)
        return db_fornecedor

    def delete (self, db_fornecedor: Fornecedor) -> None:
        self.db.delete(db_fornecedor)
        self.db.commit()