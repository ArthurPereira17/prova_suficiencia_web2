"""
Rotas de Tipo (categoria do equipamento: Computador, Impressora, etc).
GET é público; criação/edição/remoção exigem token, seguindo o mesmo padrão
usado em Equipamento.
"""
from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dao.tipo_dao import TipoDAO
from app.schemas import TipoCreate, TipoUpdate, TipoOut
from app.auth import obter_usuario_atual

router = APIRouter(prefix="/RestAPIFurb/tipos", tags=["Tipos"])


@router.get("", response_model=List[TipoOut], status_code=status.HTTP_200_OK)
def listar_tipos(db: Session = Depends(get_db)):
    return TipoDAO(db).get_all()


@router.get("/{tipo_id}", response_model=TipoOut, status_code=status.HTTP_200_OK)
def buscar_tipo(tipo_id: int, db: Session = Depends(get_db)):
    tipo = TipoDAO(db).get_by_id(tipo_id)
    if not tipo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo não encontrado")
    return tipo


@router.post("", response_model=TipoOut, status_code=status.HTTP_201_CREATED)
def criar_tipo(
    data: TipoCreate,
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(obter_usuario_atual),
):
    return TipoDAO(db).create(data)


@router.put("/{tipo_id}", response_model=TipoOut, status_code=status.HTTP_200_OK)
def atualizar_tipo(
    tipo_id: int,
    data: TipoUpdate,
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(obter_usuario_atual),
):
    dao = TipoDAO(db)
    tipo = dao.get_by_id(tipo_id)
    if not tipo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo não encontrado")
    return dao.update(tipo, data)


@router.delete("/{tipo_id}", status_code=status.HTTP_200_OK)
def remover_tipo(
    tipo_id: int,
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(obter_usuario_atual),
):
    dao = TipoDAO(db)
    tipo = dao.get_by_id(tipo_id)
    if not tipo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo não encontrado")
    dao.delete(tipo)
    return {"success": {"text": "tipo removido"}}