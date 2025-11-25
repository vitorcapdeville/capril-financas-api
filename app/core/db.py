from datetime import datetime

from sqlmodel import Session, SQLModel, create_engine, select

from app import crud, models
from app.core.config import settings
from app.models import User, UserCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def create_tables():
    SQLModel.metadata.create_all(engine)


def populate_tables(session: Session) -> None:
    fornecedor1 = models.Fornecedor(nome="Supermercado")
    fornecedor2 = models.Fornecedor(nome="Posto de gasolina")
    produto1 = models.Produto(nome="Boursin ervas", peso_em_gramas=150)
    produto2 = models.Produto(nome="Boursin ervas", peso_em_gramas=1000)
    cliente1 = models.Cliente(nome="João", email="joao@hotmail.com", categoria="pessoa física", endereco="Rua 1")

    session.add(fornecedor1)
    session.add(fornecedor2)
    session.add(produto1)
    session.add(produto2)
    session.add(cliente1)

    session.commit()

    compras = []
    compras.append(models.Compra(data_compra=datetime.now(), valor=10, categoria="insumo", fornecedor_id=1))
    compras.append(models.Compra(data_compra=datetime.now(), valor=500, categoria="combustivel", fornecedor_id=2))
    compras.append(models.Compra(data_compra=datetime.now(), valor=500, categoria="combustivel", fornecedor_id=2))
    compras.append(models.Compra(data_compra=datetime.now(), valor=500, categoria="combustivel", fornecedor_id=2))
    compras.append(models.Compra(data_compra=datetime.now(), valor=500, categoria="combustivel", fornecedor_id=2))
    compras.append(models.Compra(data_compra=datetime.now(), valor=500, categoria="combustivel", fornecedor_id=2))
    compras.append(models.Compra(data_compra=datetime.now(), valor=500, categoria="combustivel", fornecedor_id=2))
    compras.append(models.Compra(data_compra=datetime.now(), valor=500, categoria="combustivel", fornecedor_id=2))
    compras.append(models.Compra(data_compra=datetime.now(), valor=500, categoria="combustivel", fornecedor_id=2))
    compras.append(models.Compra(data_compra=datetime.now(), valor=500, categoria="combustivel", fornecedor_id=2))
    venda1 = models.Venda(data_venda=datetime(2024, 10, 30), cliente_id=1)
    item1 = models.Item(preco_unitario=10, quantidade=5, produto_id=1, venda_id=1)
    item2 = models.Item(preco_unitario=50, quantidade=1, produto_id=2, venda_id=1)

    session.add_all(compras)
    session.add(venda1)
    session.add(item1)
    session.add(item2)

    session.commit()


def create_first_user(session: Session):
    user = session.exec(select(User).where(User.email == settings.FIRST_SUPERUSER)).first()

    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)


def init_db(session: Session) -> None:
    create_tables()
    populate_tables(session)
    create_first_user(session)
