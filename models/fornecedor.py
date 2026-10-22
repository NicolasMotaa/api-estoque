from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from config.db import Base

class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    cnpj = Column(String(14), unique=True) #apenas números sem pontos, traço ou barra
    telefone = Column(String(20)) #flexível para colocar código de país, DDD ou número internacional
    email = Column(String(255), unique=True)

    produtos = relationship("Produto", back_populates="fornecedor")

