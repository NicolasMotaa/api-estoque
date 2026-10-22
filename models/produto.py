from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base


class Produto(Base):
    __tablename__="produtos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(255))
    codigo = Column(String, unique=True)
    preco_custo = Column(Numeric)
    preco_venda = Column(Numeric)
    quantidade_em_estoque = Column(Integer)
    data_cadastro = Column(Date)
    estoque_minimo = Column(Integer, default=0)

#adicionar após a criação das entidades Categoria e Fornecedor

#    #chaves estrangeiras
#    categoria_id = Column(Integer, ForeignKey("categorias_id"))
#    fornecedor_id = Column(Integer, ForeignKey("fornecedores_id"))
#
#    #relacionamentos
#    categoria = relationship("Categoria", back_populates="produtos")
#    fornecedor = relationship("Fornecedor", back_populates="produtos")