from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class FornecedorBase(SQLModel):
    nome: str = Field(unique=True, max_length=50)


class FornecedorCreate(FornecedorBase):
    pass


class Fornecedor(FornecedorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # compras: list["Compra"] = Relationship(back_populates="fornecedor")


class FornecedorPublic(FornecedorBase):
    id: int


class FornecedoresPublic(SQLModel):
    data: list[FornecedorPublic]
    count: int


class CompraBase(SQLModel):
    data_compra: datetime
    valor: float
    categoria: str


class CompraCreate(CompraBase):
    pass


class Compra(CompraBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fornecedor_id: Optional[int] = Field(default=None, foreign_key="fornecedor.id")

    fornecedor: "Fornecedor" = Relationship()


class CompraPublic(CompraBase):
    id: int
    fornecedor: FornecedorPublic


class ComprasPublic(SQLModel):
    data: list[CompraPublic]
    count: int


class ProdutoBase(SQLModel):
    nome: str
    peso_em_gramas: float


class ProdutoCreate(ProdutoBase):
    pass


class Produto(ProdutoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ProdutoPublic(ProdutoBase):
    id: int


class ProdutosPublic(SQLModel):
    data: list[ProdutoPublic]
    count: int


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


class ClientesPublic(SQLModel):
    data: list[ClientePublic]
    count: int


class ItemBase(SQLModel):
    preco_unitario: float
    quantidade: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    produto_id: int = Field(foreign_key="produto.id")
    venda_id: Optional[int] = Field(default=None, foreign_key="venda.id")

    produto: "Produto" = Relationship()


class ItemPublic(ItemBase):
    id: int

    produto: ProdutoPublic


class VendaBase(SQLModel):
    data_venda: datetime
    data_pagamento: Optional[datetime] = None


class VendaCreate(VendaBase):
    pass


class Venda(VendaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: Optional[int] = Field(default=None, foreign_key="cliente.id")

    items: list["Item"] = Relationship()
    cliente: "Cliente" = Relationship()


class VendaPublic(VendaBase):
    id: int

    items: list[ItemPublic]
    cliente: ClientePublic


class VendasPublic(SQLModel):
    data: list[VendaPublic]
    count: int


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None
    email: str | None = None


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int
