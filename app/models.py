from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Fornecedor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str


class Compra(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data_compra: datetime
    valor: float
    categoria: str

    fornecedor_id: int = Field(foreign_key="fornecedor.id")


class Produto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    peso_em_gramas: float


class Cliente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str
    categoria: str
    endereco: str


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    preco_unitario: float
    quantidade: int

    produto_id: int = Field(foreign_key="produto.id")
    venda_id: int = Field(foreign_key="venda.id")


class Venda(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data_venda: datetime
    data_pagamento: Optional[datetime] = Field(default=None)

    cliente_id: int = Field(foreign_key="cliente.id")
