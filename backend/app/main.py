"""
Ponto de entrada da API.
Documentação Swagger gerada automaticamente pelo FastAPI em /docs (requisito 4).
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app import models  # garante que os models sejam registrados antes do create_all
from app.routers import equipamentos, tipos, auth_router, usuarios

# Cria as tabelas no MySQL automaticamente a partir dos models (ORM) -- requisito 2
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RestAPIFurb - Prova de Suficiência Programação Web II",
    description=(
        "Web Service REST para controle de equipamentos, desenvolvido para a "
        "prova de suficiência de Programação Web II (FURB - 2026/2)."
    ),
    version="1.0.0",
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",
)

# Libera acesso do front-end React (rodando em outra porta) durante o desenvolvimento
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(tipos.router)
app.include_router(equipamentos.router)
app.include_router(usuarios.router)


@app.get("/", tags=["Status"])
def raiz():
    return {"status": "ok", "docs": "/docs"}