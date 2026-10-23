from pydantic import BaseModel
from typing import Optional

class CategoriaBase(BaseModel):
    nome: str

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id: int

    class Config:
        from_attributes = True

class CategoriaUpdate(BaseModel):
    nome: Optional[str] = None