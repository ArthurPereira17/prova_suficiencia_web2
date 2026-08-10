"""
Rotas de Usuario: listagem e remoção (usadas pela tela de gerenciamento de
usuários no front). Registro de novo usuário fica em auth_router.py
(/RestAPIFurb/auth/registrar), pois é usado pela tela de cadastro pública.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from lib.database import get_db
from service.userService import listar_usuarios as listar_usuarios_service, buscar_usuario_por_id, remover_usuario as remover_usuario_service
from app.schemas import UsuarioOut
from lib.auth import obter_usuario_atual

router = APIRouter(prefix="/RestAPIFurb/usuarios", tags=["Usuários"])


@router.get("", response_model=List[UsuarioOut], status_code=status.HTTP_200_OK)
def listar_usuarios(
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(obter_usuario_atual),
):
    return listar_usuarios_service(db)


@router.delete("/{usuario_id}", status_code=status.HTTP_200_OK)
def remover_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(obter_usuario_atual),
):
    usuario = buscar_usuario_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    # Evita que o usuário logado remova a própria conta sem querer
    if usuario.username == usuario_atual:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você não pode remover o próprio usuário logado",
        )

    remover_usuario_service(db, usuario)
    return {"success": {"text": "usuário removido"}}