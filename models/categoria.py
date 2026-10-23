from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from config.db import Base

class Categoria(Base):
    __tablename__= "categorias"

    id = Column(Integer, primary_key=True)
    nome = Column(String(255), unique=True)

    produtos = relationship("Produto", back_populates="categoria")