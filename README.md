# RestAPIFurb — Prova de Suficiência Programação Web II (2026/2)

Projeto feito para a prova de suficiência de Programação Web II — FURB.
Backend em **Python (FastAPI) + MySQL/MariaDB (SQLAlchemy ORM)** e frontend em **React**.

## Estrutura

```
prova-suficiencia/
├── backend/          # API REST (FastAPI)
│   ├── app/
│   │   ├── main.py           # app FastAPI, CORS, inclui os routers
│   │   ├── database.py       # conexão SQLAlchemy com o MySQL
│   │   ├── models.py         # ORM: Tipo, Equipamento, Usuario
│   │   ├── schemas.py        # validação Pydantic
│   │   ├── auth.py           # JWT (hash de senha, token)
│   │   ├── dao/               # camada DAO (acesso a dados isolado das rotas)
│   │   └── routers/           # endpoints (equipamentos, tipos, auth)
│   ├── seed.py        # popula o banco com dados de exemplo + usuário admin
│   ├── requirements.txt
│   └── .env.example
└── frontend/         # SPA em React (Vite) que consome a API
    └── src/
```

## Requisitos atendidos (conforme enunciado)

| # | Requisito | Como foi feito |
|---|---|---|
| 1 | Web Service REST + JSON + status codes corretos | FastAPI, códigos 200/201/400/401/404/422 |
| 2 | Persistência via ORM, nomenclatura padrão | SQLAlchemy — tabela `equipamentos`/`tipos` (plural), classe `Equipamento`/`Tipo` (singular) |
| 3 | Serviço protegido por token | JWT — POST/PUT/DELETE exigem `Authorization: Bearer <token>` |
| 4 | Documentação Swagger | Automática em `/docs` (FastAPI/OpenAPI) |
| 5 | Arquitetura separando modelo x serviço | Camada `dao/` (DAO) entre os `models` e os `routers` |
| 6 | Validação dos atributos | Pydantic (`schemas.py`) — nome não pode ser vazio, tamanhos mínimos/máximos, `tipo_id` obrigatório |
| 7 | Camada de Usuário extra | `Usuario` (models) + rotas `/auth/registrar` e `/auth/login` |

## Como rodar

### 1. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate          # Linux/Mac
pip install -r requirements.txt

# Configure o banco (crie um MySQL local antes)
cp .env.example .env
# edite o .env se seu usuário/senha do MySQL forem diferentes

# Cria o banco no seu MySQL (ajuste usuário/senha se necessário):
mysql -u root -e "CREATE DATABASE furb_suficiencia CHARACTER SET utf8mb4;"
mysql -u root -e "CREATE USER 'furb'@'localhost' IDENTIFIED BY 'furb123'; GRANT ALL PRIVILEGES ON furb_suficiencia.* TO 'furb'@'localhost'; FLUSH PRIVILEGES;"

# Popula com dados de exemplo + usuário admin/admin123
python seed.py

# Sobe a API em http://localhost:8080
uvicorn app.main:app --reload --port 8080
```

Depois de subir, acesse:
- **Swagger**: http://localhost:8080/docs
- **API**: http://localhost:8080/RestAPIFurb/equipamentos

### 2. Frontend

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

Acesse http://localhost:5173 e faça login com `admin` / `admin123`.

## Testando a API sem o front (Swagger ou curl)

```bash
# Login (pega o token)
curl -X POST http://localhost:8080/RestAPIFurb/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# Listar equipamentos (não precisa de token)
curl http://localhost:8080/RestAPIFurb/equipamentos

# Criar equipamento (precisa de token)
curl -X POST http://localhost:8080/RestAPIFurb/equipamentos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{"nome": "Imp HP", "tipo_id": 3}'
```

No Swagger (`/docs`) também dá pra usar o botão **Authorize** e colar usuário/senha
direto (ele já usa o endpoint de login).

## Publicando no GitHub (prazo: 12/08/2026)

```bash
cd prova-suficiencia
git init
git add .
git commit -m "Prova de suficiência - Programação Web II"
git branch -M main
git remote add origin <URL_DO_SEU_REPOSITORIO>
git push -u origin main
```

Depois envie o link do repositório para **LPA@FURB.BR**.

Veja também `NOTES-arguicao.md` com um roteiro de estudo pra arguição oral do dia 13/08.