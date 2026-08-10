from sqlalchemy import Column, Integer, String
from lib.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(60), nullable=False, unique=True, index=True)
    senha_hash = Column(String(255), nullable=False)