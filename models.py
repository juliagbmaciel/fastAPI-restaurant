import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float

engine = sqlalchemy.create_engine('sqlite:///fast_restaurantes.db', echo=True)

Base = declarative_base()


class Restaurantes(Base):
    __tablename__ = "restaurantes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100))
    descricao = Column(String(200))
    local = Column(String(100))
    imagem = Column(String(300))
    avaliacao = Column(Integer)

class Pratos(Base):
    __tablename__ = "pratos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_restaurante = Column(Integer, ForeignKey('restaurantes.id'))
    nome = Column(String(100))
    descricao = Column(String(200))
    preco = Column(Float)



Base.metadata.create_all(engine)

