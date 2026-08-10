"""Compatibilidade estrutural: o cadastro continua implementado na rota de autenticação."""
from ..login.route import router

__all__ = ["router"]