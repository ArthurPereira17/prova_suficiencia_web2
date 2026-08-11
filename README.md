# RestAPIFurb — Prova de Suficiência de Programação Web II (2026/2)

Web Service REST para controle de patrimônio (equipamentos), desenvolvido para a prova de suficiência de **Programação Web II** — FURB, seguindo o enunciado *Suficiência-ProgWebII-2026-2*.

**Stack:** Python (FastAPI) + SQLAlchemy (ORM) + MySQL/MariaDB no backend, React (Vite) no frontend, autenticação via JWT e documentação automática via Swagger/OpenAPI.

---

## Sumário

- [Arquitetura](#arquitetura)
- [Estrutura de pastas](#estrutura-de-pastas)
- [Requisitos do enunciado atendidos](#requisitos-do-enunciado-atendidos)
- [Como rodar o projeto](#como-rodar-o-projeto)
- [Endpoints da API](#endpoints-da-api)
- [Páginas do frontend](#páginas-do-frontend)
- [Segurança e variáveis de ambiente](#segurança-e-variáveis-de-ambiente)

---

## Arquitetura

O backend segue uma arquitetura em camadas, com cada uma tendo uma única responsabilidade:

```
Requisição HTTP
      │
      ▼
  route.py        → recebe a requisição, valida entrada (Pydantic), define status codes
      │
      ▼
  service/         → regra de negócio (o que pode/não pode acontecer)
      │
      ▼
  dao/              → conversa com o banco (SQLAlchemy), isolado de tudo o mais
      │
      ▼
  model/            → definição das tabelas (ORM)
      │
      ▼
    MySQL
```

Essa separação existe para que cada camada possa mudar sem afetar as outras — por exemplo, trocar MySQL por outro banco alteraria apenas `dao/`, e uma nova regra de negócio (como "não deixar o usuário se auto-remover") fica isolada em `service/`, sem misturar com a rota.

## Estrutura de pastas

```
backend/
├── app/
│   ├── main.py                    # cria a app FastAPI, CORS, registra as rotas, gera as tabelas
│   ├── models.py                  # compatibilidade: reexporta as classes de model/
│   ├── schemas.py                 # validação Pydantic (entrada) e serialização (saída)
│   ├── dao/                       # acesso a dados (SQLAlchemy) — Data Access Object
│   │   ├── equipamento_dao.py
│   │   ├── tipo_dao.py
│   │   └── usuario_dao.py
│   └── RestApiFurb/                # rotas da API, uma pasta por recurso
│       ├── equipamentos/route.py   # GET/POST/PUT/DELETE /RestAPIFurb/equipamentos
│       ├── tipos/route.py          # GET/POST/PUT/DELETE /RestAPIFurb/tipos
│       ├── login/route.py          # POST /RestAPIFurb/auth/registrar e /login
│       ├── singUp/route.py         # alias de compatibilidade para login/route.py
│       ├── users/route.py          # GET/DELETE /RestAPIFurb/usuarios
│       └── docs/route.py           # expõe o schema OpenAPI
├── lib/
│   ├── database.py                 # engine SQLAlchemy, sessão, conexão com o MySQL
│   └── auth.py                     # JWT: hash de senha, criação/validação de token
├── model/                          # classes ORM (uma tabela por classe)
│   ├── equipamentoModel.py
│   ├── tipoModel.py
│   └── userModel.py
├── service/                        # regra de negócio entre a rota e o DAO
│   ├── equipamentoService.py
│   ├── tipoService.py
│   └── userService.py
├── seed.py                         # popula o banco com dados de exemplo + usuário admin
├── requirements.txt
└── .env.example

frontend/
└── src/
    ├── api/                        # chamadas HTTP (axios) para cada recurso
    ├── components/
    │   ├── Nav.jsx                 # menu superior (nome do usuário, links, sair)
    │   └── RotaProtegida.jsx       # bloqueia rota se não estiver logado
    ├── context/AuthContext.jsx     # guarda o token JWT e o usuário logado
    └── pages/
        ├── Equipamentos.jsx        # tela pública: lista e (se logado) gerencia equipamentos
        ├── Login.jsx
        ├── Cadastro.jsx
        ├── Usuarios.jsx            # tela protegida: lista/remove usuários
        └── Docs.jsx                # atalho para o Swagger
```

> **Nota:** as pastas `dao/` (raiz de `app/`), `routers/` (vazia) e `reserva/` na raiz do projeto são versões antigas de arquivos que foram migrados para a estrutura atual (`RestApiFurb/*/route.py` + `service/` + `model/`). Elas não são importadas em nenhum lugar do código — dá para apagá-las com segurança se quiser deixar o repositório mais limpo antes da entrega.

## Requisitos do enunciado atendidos

| # | Requisito | Como foi implementado |
|---|---|---|
| 1 | Web Service REST + JSON + status codes corretos | FastAPI; `200` (GET/PUT/DELETE OK), `201` (criado), `400` (dado inválido), `401` (sem token/token inválido), `404` (não encontrado), `422` (falha de validação) |
| 2 | Persistência via ORM, nomenclatura padrão de BD | SQLAlchemy (`model/`) — tabela `equipamentos`/`tipos`/`usuarios` no plural, classe `Equipamento`/`Tipo`/`Usuario` no singular; tabelas geradas automaticamente via `Base.metadata.create_all` |
| 3 | Serviço protegido por token | JWT (`lib/auth.py`) — POST/PUT/DELETE de equipamentos, tipos e usuários exigem `Authorization: Bearer <token>` |
| 4 | Documentação via Swagger | Automática em `/docs` (FastAPI/OpenAPI), com atalho na tela **Docs** do frontend |
| 5 | Arquitetura separando modelo dos serviços | `model/` (estrutura da tabela) → `dao/` (acesso a dados) → `service/` (regra de negócio) → `route.py` (HTTP) |
| 6 | Validação dos atributos | Pydantic (`app/schemas.py`) — nome não pode ser vazio, tamanhos mínimos/máximos, `tipo_id` obrigatório e validado contra o banco |
| 7 | Camada de Usuário extra | `Usuario` (model) + rotas de registro, login, listagem e remoção |

## Como rodar o projeto

### 1. Banco de dados

Crie o banco e um usuário no seu MySQL/MariaDB local (ajuste usuário/senha conforme preferir):

```sql
CREATE DATABASE furb_suficiencia CHARACTER SET utf8mb4;
CREATE USER 'furb'@'localhost' IDENTIFIED BY 'sua_senha_aqui';
GRANT ALL PRIVILEGES ON furb_suficiencia.* TO 'furb'@'localhost';
FLUSH PRIVILEGES;
```

### 2. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate          # Linux/Mac
pip install -r requirements.txt

cp .env.example .env
# edite o .env com o usuário/senha que você criou no passo 1

python seed.py                    # popula dados de exemplo + usuário admin/admin123
uvicorn app.main:app --reload --port 8080
```

- **API:** http://localhost:8080/RestAPIFurb/equipamentos
- **Swagger:** http://localhost:8080/docs

### 3. Frontend

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

Acesse http://localhost:5173. Sem login, só é possível visualizar os equipamentos; após logar (`admin` / `admin123`, ou criando uma conta em **Cadastrar**), aparecem as opções de gerenciar equipamentos, tipos e usuários.

## Endpoints da API

Prefixo base: `http://localhost:8080/RestAPIFurb`

| Método | Rota | Autenticação | Descrição |
|---|---|---|---|
| `GET` | `/equipamentos` | Não | Lista todos os equipamentos |
| `GET` | `/equipamentos/{id}` | Não | Busca um equipamento |
| `POST` | `/equipamentos` | Sim | Cria um equipamento |
| `PUT` | `/equipamentos/{id}` | Sim | Atualiza campos enviados (parcial) |
| `DELETE` | `/equipamentos/{id}` | Sim | Remove um equipamento |
| `GET` | `/tipos` | Não | Lista todos os tipos |
| `GET` | `/tipos/{id}` | Não | Busca um tipo |
| `POST` | `/tipos` | Sim | Cria um tipo |
| `PUT` | `/tipos/{id}` | Sim | Atualiza um tipo |
| `DELETE` | `/tipos/{id}` | Sim | Remove um tipo |
| `POST` | `/auth/registrar` | Não | Cria uma nova conta de usuário |
| `POST` | `/auth/login` | Não | Autentica e devolve um token JWT |
| `GET` | `/usuarios` | Sim | Lista os usuários cadastrados |
| `DELETE` | `/usuarios/{id}` | Sim | Remove um usuário (não permite auto-remoção) |
| `GET` | `/docs` | Não | Schema OpenAPI cru (JSON) |

Autenticação: envie `Authorization: Bearer <token>` no header, onde `<token>` vem da resposta de `/auth/login`.

## Páginas do frontend

| Rota | Acesso | Descrição |
|---|---|---|
| `/` | Pública | Lista de equipamentos; formulário de criar/editar/remover só aparece logado |
| `/login` | Pública | Login |
| `/cadastro` | Pública | Criação de conta (loga automaticamente após cadastrar) |
| `/docs` | Pública | Atalho para o Swagger da API |
| `/usuarios` | Protegida | Lista de usuários com opção de remover (redireciona para `/login` se não estiver autenticado) |

## Segurança e variáveis de ambiente

O arquivo `backend/.env.example` deste projeto está com valores reais preenchidos (senha do MySQL e uma `JWT_SECRET_KEY` fraca), e não existe um `.gitignore` na raiz. Antes de subir para o GitHub, vale a pena:

- Criar um `.gitignore` (excluindo `.env`, `venv/`, `node_modules/`, `__pycache__/`)
- Trocar `.env.example` para conter apenas placeholders (ex: `DB_PASSWORD=sua_senha_aqui`)
- Gerar uma `JWT_SECRET_KEY` mais forte, por exemplo com `python -c "import secrets; print(secrets.token_hex(32))"`

Isso evita expor sua senha do banco publicamente no repositório da prova.
