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

from app.database import get_db
from app.dao.equipamento_dao import EquipamentoDAO
from app.dao.tipo_dao import TipoDAO
from app.schemas import EquipamentoCreate, EquipamentoUpdate, EquipamentoOut
from app.auth import obter_usuario_atual

router = APIRouter(prefix="/RestAPIFurb/equipamentos", tags=["Equipamentos"])


@router.get("", status_code=status.HTTP_200_OK)
def listar_equipamentos(db: Session = Depends(get_db)) -> Dict:
    dao = EquipamentoDAO(db)
    equipamentos = dao.get_all()
    return {"equipamentos": [EquipamentoOut.model_validate(e) for e in equipamentos]}


@router.get("/{equipamento_id}", response_model=EquipamentoOut, status_code=status.HTTP_200_OK)
def buscar_equipamento(equipamento_id: int, db: Session = Depends(get_db)):
    dao = EquipamentoDAO(db)
    equipamento = dao.get_by_id(equipamento_id)
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
    dao = EquipamentoDAO(db)
    return dao.create(data)


@router.put("/{equipamento_id}", response_model=EquipamentoOut, status_code=status.HTTP_200_OK)
def atualizar_equipamento(
    equipamento_id: int,
    data: EquipamentoUpdate,
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(obter_usuario_atual),
):
    dao = EquipamentoDAO(db)
    equipamento = dao.get_by_id(equipamento_id)
    if not equipamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipamento não encontrado")

    if data.tipo_id is not None:
        tipo_dao = TipoDAO(db)
        if not tipo_dao.get_by_id(data.tipo_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="tipo_id inválido")

    return dao.update(equipamento, data)


@router.delete("/{equipamento_id}", status_code=status.HTTP_200_OK)
def remover_equipamento(
    equipamento_id: int,
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(obter_usuario_atual),
):
    dao = EquipamentoDAO(db)
    equipamento = dao.get_by_id(equipamento_id)
    if not equipamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipamento não encontrado")
    dao.delete(equipamento)
    return {"success": {"text": "equipamento removido"}}