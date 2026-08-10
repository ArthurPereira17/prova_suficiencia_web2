"""
Rotas de Usuario: listagem e remoção (usadas pela tela de gerenciamento de
usuários no front). Registro de novo usuário fica em auth_router.py
(/RestAPIFurb/auth/registrar), pois é usado pela tela de cadastro pública.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dao.usuario_dao import UsuarioDAO
from app.schemas import UsuarioOut
from app.auth import obter_usuario_atual

router = APIRouter(prefix="/RestAPIFurb/usuarios", tags=["Usuários"])


@router.get("", response_model=List[UsuarioOut], status_code=status.HTTP_200_OK)
def listar_usuarios(
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(obter_usuario_atual),
):
    return UsuarioDAO(db).get_all()


@router.delete("/{usuario_id}", status_code=status.HTTP_200_OK)
def remover_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(obter_usuario_atual),
):
    dao = UsuarioDAO(db)
    usuario = dao.get_by_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    # Evita que o usuário logado remova a própria conta sem querer
    if usuario.username == usuario_atual:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você não pode remover o próprio usuário logado",
        )

    dao.delete(usuario)
    return {"success": {"text": "usuário removido"}}