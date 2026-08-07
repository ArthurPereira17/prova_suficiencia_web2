"""
Models (entidades) mapeadas via SQLAlchemy ORM.
Nomenclatura padrão de BD: tabela no plural, classe no singular.
As tabelas/colunas são geradas automaticamente pelo framework (Base.metadata.create_all).
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Tipo(Base):
    __tablename__ = "tipos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(80), nullable=False, unique=True)

    equipamentos = relationship("Equipamento", back_populates="tipo")


class Equipamento(Base):
    __tablename__ = "equipamentos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(120), nullable=False)
    tipo_id = Column(Integer, ForeignKey("tipos.id"), nullable=False)

    tipo = relationship("Tipo", back_populates="equipamentos")


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(60), nullable=False, unique=True, index=True)
    senha_hash = Column(String(255), nullable=False)