from pydantic import BaseModel
from datetime import date
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str
    codigo: str
    preco_custo: float
    preco_venda: float
    quantidade_em_estoque: int
    categoria_id: int
    fornecedor_id: int
    estoque_minimo: int

#RequestDTO
class ProdutoCreate(ProdutoBase):
    pass

#ResponseDTO
class ProdutoResponse(ProdutoBase):
    id: int
    data_cadastro: date

    class Config:
        from_attributes = True #Faz o Pydantic ler objetos do SQLAlchemy

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    codigo: Optional[int] = None
    preco_custo: Optional[float] = None
    preco_venda: Optional[float] = None
    quantidade_em_estoque: Optional[int] = None
    estoque_minimo: Optional[int] = None