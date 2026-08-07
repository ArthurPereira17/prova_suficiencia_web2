"""
Schemas Pydantic: validam os dados de entrada (requisito 6 do enunciado)
e definem o formato JSON de saída das respostas.
"""
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator


# ---------- Tipo ----------
class TipoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=80)

    @field_validator("nome")
    @classmethod
    def nome_nao_vazio(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("nome não pode ser vazio")
        return v


class TipoCreate(TipoBase):
    pass


class TipoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=80)


class TipoOut(TipoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------- Equipamento ----------
class EquipamentoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=120)
    tipo_id: int = Field(..., gt=0)

    @field_validator("nome")
    @classmethod
    def nome_nao_vazio(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("nome não pode ser vazio")
        return v


class EquipamentoCreate(EquipamentoBase):
    pass


class EquipamentoUpdate(BaseModel):
    """PUT parcial: só o que for enviado é alterado (requisito do enunciado)."""
    nome: Optional[str] = Field(None, min_length=2, max_length=120)
    tipo_id: Optional[int] = Field(None, gt=0)

    @field_validator("nome")
    @classmethod
    def nome_nao_vazio(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("nome não pode ser vazio")
        return v


class EquipamentoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    tipo: TipoOut


# ---------- Usuário / Auth ----------
class UsuarioCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=60)
    senha: str = Field(..., min_length=4, max_length=100)


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"