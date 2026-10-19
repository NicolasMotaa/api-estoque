from sqlalchemy import Column, Integer, String, Numeric, Date
from config.db import Base


class Produto(Base):
    __tablename__="produtos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(255))
    codigo = Column(Integer, unique=True)
    preco_custo = Column(Numeric)
    preco_venda = Column(Numeric)
    quantidade_em_estoque = Column(Integer)
    data_cadastro = Column(Date)
