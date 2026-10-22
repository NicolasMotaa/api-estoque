from pydantic import BaseModel
from typing import Optional

class FornecedorBase(BaseModel):
    nome: str
    telefone: str
    email: str
    #cnpj disponível apenas na criação e no response, pois empresas não mudam de cnpj
    #novo cnpj = nova empresa

class FornecedorCreate(FornecedorBase):
    cnpj: str
    pass

class FornecedorResponse(FornecedorBase):
    id: int
    cnpj: str

    class Config:
        from_attributes = True

class FornecedorUpdate(FornecedorBase):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None