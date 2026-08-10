"""Serviços de Equipamento: camada entre as rotas e os DAOs."""
from app.dao.equipamento_dao import EquipamentoDAO
from app.schemas import EquipamentoCreate, EquipamentoUpdate


def listar_equipamentos(db):
    return EquipamentoDAO(db).get_all()


def buscar_equipamento_por_id(db, equipamento_id: int):
    return EquipamentoDAO(db).get_by_id(equipamento_id)


def criar_equipamento(db, data: EquipamentoCreate):
    return EquipamentoDAO(db).create(data)


def atualizar_equipamento(db, equipamento, data: EquipamentoUpdate):
    return EquipamentoDAO(db).update(equipamento, data)


def remover_equipamento(db, equipamento):
    EquipamentoDAO(db).delete(equipamento)