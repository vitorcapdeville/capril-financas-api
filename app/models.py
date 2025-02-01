from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class FornecedorBase(SQLModel):
    nome: str = Field(unique=True, min_length=1, max_length=50)


class FornecedorCreate(FornecedorBase):
    pass


class Fornecedor(FornecedorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # compras: list["Compra"] = Relationship(back_populates="fornecedor")


class FornecedorPublic(FornecedorBase):
    id: int


class CompraBase(SQLModel):
    data_compra: datetime
    valor: float = Field(gt=0)
    categoria: str = Field(min_length=1)


class CompraCreate(CompraBase):
    fornecedor_id: int


class Compra(CompraBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fornecedor_id: Optional[int] = Field(default=None, foreign_key="fornecedor.id")

    fornecedor: "Fornecedor" = Relationship()


class CompraPublic(CompraBase):
    id: int
    fornecedor: FornecedorPublic


class ProdutoBase(SQLModel):
    nome: str = Field(min_length=1)
    peso_em_gramas: float = Field(gt=0)


class ProdutoCreate(ProdutoBase):
    pass


class Produto(ProdutoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ProdutoPublic(ProdutoBase):
    id: int


class ClienteBase(SQLModel):
    nome: str = Field(min_length=1)
    email: EmailStr = Field(min_length=1)
    categoria: str = Field(min_length=1)
    endereco: str = Field(min_length=1)


class ClienteCreate(ClienteBase):
    pass


class Cliente(ClienteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ClientePublic(ClienteBase):
    id: int


class ItemBase(SQLModel):
    preco_unitario: float = Field(gt=0)
    quantidade: int = Field(gt=0)


class ItemCreate(ItemBase):
    produto_id: int


class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    produto_id: int = Field(foreign_key="produto.id")
    venda_id: Optional[int] = Field(default=None, foreign_key="venda.id")

    produto: "Produto" = Relationship()
    venda: "Venda" = Relationship(back_populates="items")


class ItemPublic(ItemBase):
    id: int

    produto: ProdutoPublic


class VendaBase(SQLModel):
    data_venda: datetime
    data_pagamento: Optional[datetime] = None


class VendaCreate(VendaBase):
    cliente_id: int

    items: list[ItemCreate]


class Venda(VendaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: Optional[int] = Field(default=None, foreign_key="cliente.id")

    items: list["Item"] = Relationship(back_populates="venda")
    cliente: "Cliente" = Relationship()


class VendaPublic(VendaBase):
    id: int

    items: list[ItemPublic]
    cliente: ClientePublic


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None
    email: str | None = None


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


class UserPublic(UserBase):
    id: int
