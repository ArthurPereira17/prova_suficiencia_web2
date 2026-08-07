"""
DAO (Data Access Object) de Equipamento.
"""
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models import Equipamento
from app.schemas import EquipamentoCreate, EquipamentoUpdate


class EquipamentoDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Equipamento]:
        return (
            self.db.query(Equipamento)
            .options(joinedload(Equipamento.tipo))
            .all()
        )

    def get_by_id(self, equipamento_id: int) -> Optional[Equipamento]:
        return (
            self.db.query(Equipamento)
            .options(joinedload(Equipamento.tipo))
            .filter(Equipamento.id == equipamento_id)
            .first()
        )

    def create(self, data: EquipamentoCreate) -> Equipamento:
        equipamento = Equipamento(nome=data.nome, tipo_id=data.tipo_id)
        self.db.add(equipamento)
        self.db.commit()
        self.db.refresh(equipamento)
        return equipamento

    def update(self, equipamento: Equipamento, data: EquipamentoUpdate) -> Equipamento:
        """Atualização parcial: só altera os campos enviados (demais permanecem)."""
        if data.nome is not None:
            equipamento.nome = data.nome
        if data.tipo_id is not None:
            equipamento.tipo_id = data.tipo_id
        self.db.commit()
        self.db.refresh(equipamento)
        return equipamento

    def delete(self, equipamento: Equipamento) -> None:
        self.db.delete(equipamento)
        self.db.commit()