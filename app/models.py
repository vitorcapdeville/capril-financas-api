from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class FornecedorBase(SQLModel):
    nome: str


class FornecedorCreate(FornecedorBase):
    pass


class Fornecedor(FornecedorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class FornecedorPublic(FornecedorBase):
    id: int


class Compra(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data_compra: datetime
    valor: float
    categoria: str

    fornecedor_id: int = Field(foreign_key="fornecedor.id")


class ProdutoBase(SQLModel):
    nome: str
    peso_em_gramas: float


class ProdutoCreate(ProdutoBase):
    pass


class Produto(ProdutoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ProdutoPublic(ProdutoBase):
    id: int


class ClienteBase(SQLModel):
    nome: str
    email: str
    categoria: str
    endereco: str


class ClienteCreate(ClienteBase):
    pass


class Cliente(ClienteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ClientePublic(ClienteBase):
    id: int


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    preco_unitario: float
    quantidade: int

    produto_id: int = Field(foreign_key="produto.id")
    venda_id: int = Field(foreign_key="venda.id")


class Venda(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data_venda: datetime
    data_pagamento: Optional[datetime] = None

    cliente_id: int = Field(foreign_key="cliente.id")
