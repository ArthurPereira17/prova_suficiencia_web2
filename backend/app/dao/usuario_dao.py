"""
DAO (Data Access Object) de Usuario (usado pela autenticação).
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models import Usuario


class UsuarioDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.username == username).first()

    def create(self, username: str, senha_hash: str) -> Usuario:
        usuario = Usuario(username=username, senha_hash=senha_hash)
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario