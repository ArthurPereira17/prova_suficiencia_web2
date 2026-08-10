"""Serviços de Tipo: camada entre as rotas e os DAOs."""
from app.dao.tipo_dao import TipoDAO
from app.schemas import TipoCreate, TipoUpdate


def listar_tipos(db):
    return TipoDAO(db).get_all()


def buscar_tipo_por_id(db, tipo_id: int):
    return TipoDAO(db).get_by_id(tipo_id)


def criar_tipo(db, data: TipoCreate):
    return TipoDAO(db).create(data)


def atualizar_tipo(db, tipo, data: TipoUpdate):
    return TipoDAO(db).update(tipo, data)


def remover_tipo(db, tipo):
    TipoDAO(db).delete(tipo)