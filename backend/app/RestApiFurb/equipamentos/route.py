"""
Rotas de Equipamento.

GET  /RestAPIFurb/equipamentos       -> público
GET  /RestAPIFurb/equipamentos/{id}  -> público
POST /RestAPIFurb/equipamentos       -> requer token (JWT)
PUT  /RestAPIFurb/equipamentos/{id}  -> requer token (JWT), atualização parcial
DELETE /RestAPIFurb/equipamentos/{id}-> requer token (JWT)
"""
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from lib.database import get_db
from service.equipamentoService import (listar_equipamentos as listar_equipamentos_service, buscar_equipamento_por_id, criar_equipamento as criar_equipamento_service, atualizar_equipamento as atualizar_equipamento_service, remover_equipamento as remover_equipamento_service)
from app.dao.tipo_dao import TipoDAO
from app.schemas import EquipamentoCreate, EquipamentoUpdate, EquipamentoOut
from lib.auth import obter_usuario_atual

router = APIRouter(prefix="/RestAPIFurb/equipamentos", tags=["Equipamentos"])


@router.get("", status_code=status.HTTP_200_OK)
def listar_equipamentos(db: Session = Depends(get_db)) -> Dict:
    equipamentos = listar_equipamentos_service(db)
    return {"equipamentos": [EquipamentoOut.model_validate(e) for e in equipamentos]}


@router.get("/{equipamento_id}", response_model=EquipamentoOut, status_code=status.HTTP_200_OK)
def buscar_equipamento(equipamento_id: int, db: Session = Depends(get_db)):
    equipamento = buscar_equipamento_por_id(db, equipamento_id)
    if not equipamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipamento não encontrado")
    return equipamento


@router.post("", response_model=EquipamentoOut, status_code=status.HTTP_201_CREATED)
def criar_equipamento(
    data: EquipamentoCreate,
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(obter_usuario_atual),
):
    tipo_dao = TipoDAO(db)
    if not tipo_dao.get_by_id(data.tipo_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="tipo_id inválido")
    return criar_equipamento_service(db, data)


@router.put("/{equipamento_id}", response_model=EquipamentoOut, status_code=status.HTTP_200_OK)
def atualizar_equipamento(
    equipamento_id: int,
    data: EquipamentoUpdate,
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(obter_usuario_atual),
):
    equipamento = buscar_equipamento_por_id(db, equipamento_id)
    if not equipamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipamento não encontrado")

    if data.tipo_id is not None:
        tipo_dao = TipoDAO(db)
        if not tipo_dao.get_by_id(data.tipo_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="tipo_id inválido")

    return atualizar_equipamento_service(db, equipamento, data)


@router.delete("/{equipamento_id}", status_code=status.HTTP_200_OK)
def remover_equipamento(
    equipamento_id: int,
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(obter_usuario_atual),
):
    equipamento = buscar_equipamento_por_id(db, equipamento_id)
    if not equipamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipamento não encontrado")
    remover_equipamento_service(db, equipamento)
    return {"success": {"text": "equipamento removido"}}