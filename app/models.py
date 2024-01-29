from datetime import datetime

from sqlmodel import Field, SQLModel


class Fornecedor(SQLModel, table=True):
    nome: str = Field(primary_key=True)
    categoria: str


class Insumo(SQLModel, table=True):
    nome: str = Field(primary_key=True)
    preco_compra: float


class Produto(SQLModel, table=True):
    nome: str = Field(primary_key=True)
    preco_venda: float


class CompraInsumo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    insumo: int = Field(foreign_key="insumo.nome")
    quantidade: int
    data_compra: datetime


class VendaProduto(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    produto: int = Field(foreign_key="produto.nome")
    quantidade: int
    data_venda: datetime
