import enum
from sqlalchemy import Column, Integer, Enum as SQLAlchemyEnum, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from config.db import Base

#Enum traz a restrição de tipos, só pode ser entrada ou saída
class Tipo(str, enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"
    

class Movimentacao(Base):
    __tablename__="movimentacoes"

    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    tipo = Column(SQLAlchemyEnum(Tipo), nullable=False)
    quantidade = Column(Integer, nullable=False)
    data = Column(DateTime, default= datetime.now)

    produto = relationship("Produto", back_populates="movimentacoes")
    
