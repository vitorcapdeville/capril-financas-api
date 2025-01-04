from datetime import datetime

from sqlmodel import Session, SQLModel, create_engine

from . import models
from .config import Settings

connect_args = {"check_same_thread": False}
engine = create_engine(Settings().DATABASE_URL, connect_args=connect_args)


def create_tables():
    SQLModel.metadata.create_all(engine)


def populate_tables():
    fornecedor1 = models.Fornecedor(nome="Supermercado")
    fornecedor2 = models.Fornecedor(nome="Posto de gasolina")
    produto1 = models.Produto(nome="Boursin ervas", peso_em_gramas=150)
    produto2 = models.Produto(nome="Boursin ervas", peso_em_gramas=1000)
    cliente1 = models.Cliente(nome="João", email="joao@hotmail.com", categoria="pessoa física", endereco="Rua 1")

    with Session(engine) as session:
        session.add(fornecedor1)
        session.add(fornecedor2)
        session.add(produto1)
        session.add(produto2)
        session.add(cliente1)

        session.commit()

    compra1 = models.Compra(data_compra=datetime.now(), valor=10, categoria="insumo", fornecedor_id=1)
    compra2 = models.Compra(data_compra=datetime.now(), valor=500, categoria="combustivel", fornecedor_id=2)
    venda1 = models.Venda(data_venda=datetime(2024, 10, 30), cliente_id=1)
    item1 = models.Item(preco_unitario=10, quantidade=5, produto_id=1, venda_id=1)
    item2 = models.Item(preco_unitario=50, quantidade=1, produto_id=2, venda_id=1)

    with Session(engine) as session:
        session.add(compra1)
        session.add(compra2)
        session.add(venda1)
        session.add(item1)
        session.add(item2)

        session.commit()
