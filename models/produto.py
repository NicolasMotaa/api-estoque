from sqlalchemy import Column, Integer, String, Numeric, Date
from sqlalchemy.orm import declarative_base
from config.db import engine

Base = declarative_base()

class Produto(Base):
    __tablename__="produtos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(255))
    codigo = Column(Integer, unique=True)
    preco_custo = Column(Numeric)
    preco_venda = Column(Numeric)
    quantidade_em_estoque = Column(Integer)
    data_cadastro = Column(Date)

Base.metadata.create_all(engine)