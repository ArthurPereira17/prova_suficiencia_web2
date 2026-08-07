"""
DAO (Data Access Object) de Tipo: isola todo o acesso a dados (SQLAlchemy)
da camada de serviço/rotas, conforme requisito 5 do enunciado.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Tipo
from app.schemas import TipoCreate, TipoUpdate


class TipoDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Tipo]:
        return self.db.query(Tipo).all()

    def get_by_id(self, tipo_id: int) -> Optional[Tipo]:
        return self.db.query(Tipo).filter(Tipo.id == tipo_id).first()

    def create(self, tipo_data: TipoCreate) -> Tipo:
        tipo = Tipo(nome=tipo_data.nome)
        self.db.add(tipo)
        self.db.commit()
        self.db.refresh(tipo)
        return tipo

    def update(self, tipo: Tipo, tipo_data: TipoUpdate) -> Tipo:
        if tipo_data.nome is not None:
            tipo.nome = tipo_data.nome
        self.db.commit()
        self.db.refresh(tipo)
        return tipo

    def delete(self, tipo: Tipo) -> None:
        self.db.delete(tipo)
        self.db.commit()