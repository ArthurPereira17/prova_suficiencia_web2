"""
Rotas de Tipo (categoria do equipamento: Computador, Impressora, etc).
GET é público; criação/edição/remoção exigem token, seguindo o mesmo padrão
usado em Equipamento.
"""
from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from lib.database import get_db
from service.tipoService import (listar_tipos as listar_tipos_service, buscar_tipo_por_id, criar_tipo as criar_tipo_service, atualizar_tipo as atualizar_tipo_service, remover_tipo as remover_tipo_service)
from app.schemas import TipoCreate, TipoUpdate, TipoOut
from lib.auth import obter_usuario_atual

router = APIRouter(prefix="/RestAPIFurb/tipos", tags=["Tipos"])


@router.get("", response_model=List[TipoOut], status_code=status.HTTP_200_OK)
def listar_tipos(db: Session = Depends(get_db)):
    return listar_tipos_service(db)


@router.get("/{tipo_id}", response_model=TipoOut, status_code=status.HTTP_200_OK)
def buscar_tipo(tipo_id: int, db: Session = Depends(get_db)):
    tipo = buscar_tipo_por_id(db, tipo_id)
    if not tipo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo não encontrado")
    return tipo


@router.post("", response_model=TipoOut, status_code=status.HTTP_201_CREATED)
def criar_tipo(
    data: TipoCreate,
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(obter_usuario_atual),
):
    return criar_tipo_service(db, data)


@router.put("/{tipo_id}", response_model=TipoOut, status_code=status.HTTP_200_OK)
def atualizar_tipo(
    tipo_id: int,
    data: TipoUpdate,
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(obter_usuario_atual),
):
    tipo = buscar_tipo_por_id(db, tipo_id)
    if not tipo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo não encontrado")
    return atualizar_tipo_service(db, tipo, data)


@router.delete("/{tipo_id}", status_code=status.HTTP_200_OK)
def remover_tipo(
    tipo_id: int,
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(obter_usuario_atual),
):
    tipo = buscar_tipo_por_id(db, tipo_id)
    if not tipo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo não encontrado")
    remover_tipo_service(db, tipo)
    return {"success": {"text": "tipo removido"}}