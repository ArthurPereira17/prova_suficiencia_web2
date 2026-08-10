"""
Popula o banco com dados de exemplo (iguais aos do enunciado) e cria um
usuário de teste para autenticação.
Rodar com: python seed.py
"""
from lib.database import SessionLocal, Base, engine
from app.models import Tipo, Equipamento, Usuario
from lib.auth import hash_senha

Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    if db.query(Tipo).count() == 0:
        computador = Tipo(nome="Computador")
        audiovisual = Tipo(nome="audiovisual")
        impressora = Tipo(nome="Impressora")
        db.add_all([computador, audiovisual, impressora])
        db.commit()

        db.add_all([
            Equipamento(nome="Notebook Dell", tipo_id=computador.id),
            Equipamento(nome="Projetor Epson", tipo_id=audiovisual.id),
            Equipamento(nome="Notebook Lenovo", tipo_id=computador.id),
        ])
        db.commit()
        print("Tipos e equipamentos de exemplo criados.")
    else:
        print("Já existem tipos cadastrados, pulando seed de equipamentos.")

    if db.query(Usuario).filter(Usuario.username == "admin").first() is None:
        db.add(Usuario(username="admin", senha_hash=hash_senha("admin123")))
        db.commit()
        print("Usuário de teste criado -> username: admin / senha: admin123")
    else:
        print("Usuário 'admin' já existe.")
finally:
    db.close()