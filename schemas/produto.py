from pydantic import BaseModel
from datetime import date

class ProdutoBase(BaseModel):
    nome: str
    codigo: int
    preco_custo: float
    preco_venda: float
    quantidade_em_estoque: int
    categoria_id: int
    fornecedor_id: int

#RequestDTO
class ProdutoCreate(ProdutoBase):
    pass

#ResponseDTO
class ProdutoResponse(ProdutoBase):
    id: int
    data_cadastro: date

    class Config:
        from_attributes: True #Faz o Pydantic ler objetos do SQLAlchemy