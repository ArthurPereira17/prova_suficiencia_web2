"""
Rotas de autenticação: registro de usuário e login (emite o token JWT).
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.dao.usuario_dao import UsuarioDAO
from app.schemas import UsuarioCreate, UsuarioOut, Token
from app.auth import hash_senha, verificar_senha, criar_access_token

router = APIRouter(prefix="/RestAPIFurb/auth", tags=["Autenticação"])


@router.post("/registrar", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def registrar(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    dao = UsuarioDAO(db)
    if dao.get_by_username(usuario.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Usuário já existe")
    novo = dao.create(usuario.username, hash_senha(usuario.senha))
    return novo


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Recebe username/password (form, padrão OAuth2) e devolve um JWT.
    No Swagger: use o botão 'Authorize' e informe usuário/senha nesse formulário.
    """
    dao = UsuarioDAO(db)
    usuario = dao.get_by_username(form_data.username)
    if not usuario or not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = criar_access_token(data={"sub": usuario.username})
    return Token(access_token=token)