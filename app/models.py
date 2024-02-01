from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Fornecedor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    categoria: str


class Insumo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str


class Produto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str


class CompraInsumo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    preco_unitario: float
    quantidade: int
    data_compra: datetime

    insumo_id: int = Field(foreign_key="insumo.id")
    insumo: Insumo = Relationship()


class VendaProduto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    preco_unitario: float
    quantidade: int
    data_venda: datetime

    produto_id: int = Field(foreign_key="produto.id")
    produto: Produto = Relationship()
