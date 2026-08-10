from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from lib.database import Base


class Tipo(Base):
    __tablename__ = "tipos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(80), nullable=False, unique=True)

    equipamentos = relationship("Equipamento", back_populates="tipo")