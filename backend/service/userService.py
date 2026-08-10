"""Serviços de Usuário: camada entre as rotas e os DAOs."""
from app.dao.usuario_dao import UsuarioDAO


def listar_usuarios(db):
    return UsuarioDAO(db).get_all()


def buscar_usuario_por_id(db, usuario_id: int):
    return UsuarioDAO(db).get_by_id(usuario_id)


def buscar_usuario_por_username(db, username: str):
    return UsuarioDAO(db).get_by_username(username)


def criar_usuario(db, username: str, senha_hash: str):
    return UsuarioDAO(db).create(username, senha_hash)


def remover_usuario(db, usuario):
    UsuarioDAO(db).delete(usuario)