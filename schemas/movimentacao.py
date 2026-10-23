from pydantic import BaseModel
from datetime import datetime
from models.movimentacao import Tipo

class MovimentacaoBase(BaseModel):
    produto_id : int
    tipo : Tipo
    quantidade : int

class MovimentacaoCreate(MovimentacaoBase):
    pass

class MovimentacaoResponse(BaseModel):
    id: int
    data: datetime

    class Config:
        from_attributes = True

#Não há um schema para update pois movimentações são registros imutáveis

