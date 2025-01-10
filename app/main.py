from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import database_exists
from sqlmodel import Session, select

from .database import engine, init_database
from .dependencies import get_session
from .models import (
    Cliente,
    ClienteCreate,
    ClientePublic,
    Compra,
    CompraCreate,
    CompraPublic,
    Fornecedor,
    FornecedorCreate,
    FornecedorPublic,
    Item,
    ItemCreate,
    Produto,
    ProdutoCreate,
    ProdutoPublic,
    Venda,
    VendaCreate,
    VendaPublic,
)

if not database_exists(engine.url):
    init_database()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/fornecedores")
def read_fornecedores(session: Annotated[Session, Depends(get_session)]) -> list[FornecedorPublic]:
    fornecedores = session.exec(select(Fornecedor)).all()
    return fornecedores


@app.post("/fornecedor")
def cadastrar_fornecedor(
    fornecedor: FornecedorCreate, session: Annotated[Session, Depends(get_session)]
) -> FornecedorPublic:
    db_fornecedor = Fornecedor.model_validate(fornecedor)
    try:
        session.add(db_fornecedor)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Já existe um fornecedor com esse nome.")
    session.refresh(db_fornecedor)
    return db_fornecedor


@app.delete("/fornecedor/{fornecedor_id}")
def delete_fornecedor(fornecedor_id: int, session: Annotated[Session, Depends(get_session)]) -> FornecedorPublic:
    fornecedor = session.get(Fornecedor, fornecedor_id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado.")
    session.delete(fornecedor)
    session.commit()
    return fornecedor


@app.get("/produtos")
def read_produtos(session: Annotated[Session, Depends(get_session)]) -> list[ProdutoPublic]:
    produtos = session.exec(select(Produto)).all()
    return produtos


@app.get("/produto/{produto_id}")
def read_produto(produto_id: int, session: Annotated[Session, Depends(get_session)]) -> ProdutoPublic:
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return produto


@app.post("/produto")
def cadastrar_produto(produto: ProdutoCreate, session: Annotated[Session, Depends(get_session)]) -> ProdutoPublic:
    db_produto = Produto.model_validate(produto)
    try:
        session.add(db_produto)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Já existe um produto com esse nome.")
    session.refresh(db_produto)
    return db_produto


@app.delete("/produto/{produto_id}")
def delete_produto(produto_id: int, session: Annotated[Session, Depends(get_session)]) -> ProdutoPublic:
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    session.delete(produto)
    session.commit()
    return produto


@app.get("/clientes")
def read_clientes(session: Annotated[Session, Depends(get_session)]) -> list[ClientePublic]:
    clientes = session.exec(select(Cliente)).all()
    return clientes


@app.get("/cliente/{cliente_id}")
def read_cliente(cliente_id: int, session: Annotated[Session, Depends(get_session)]) -> ClientePublic:
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return cliente


@app.post("/cliente")
def cadastrar_cliente(cliente: ClienteCreate, session: Annotated[Session, Depends(get_session)]) -> ClientePublic:
    db_cliente = Cliente.model_validate(cliente)
    try:
        session.add(db_cliente)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Já existe um cliente com esse nome.")
    session.refresh(db_cliente)
    return db_cliente


@app.delete("/cliente/{cliente_id}")
def delete_cliente(cliente_id: int, session: Annotated[Session, Depends(get_session)]) -> ClientePublic:
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    session.delete(cliente)
    session.commit()
    return cliente


@app.get("/compras")
def read_compras(session: Annotated[Session, Depends(get_session)]) -> list[CompraPublic]:
    compras = session.exec(select(Compra)).all()
    return compras


@app.get("/compra/{compra_id}")
def read_compra(compra_id: int, session: Annotated[Session, Depends(get_session)]) -> CompraPublic:
    compra = session.get(Compra, compra_id)
    if not compra:
        raise HTTPException(status_code=404, detail="Compra não encontrada.")
    return compra


@app.post("/compra")
def cadastrar_compra(compra: CompraCreate, session: Annotated[Session, Depends(get_session)]) -> CompraPublic:
    db_compra = Compra.model_validate(compra)
    session.add(db_compra)
    session.commit()
    session.refresh(db_compra)
    return db_compra


@app.get("/vendas")
def read_vendas(session: Annotated[Session, Depends(get_session)]) -> list[VendaPublic]:
    vendas = session.exec(select(Venda)).all()
    return vendas


@app.get("/venda/{venda_id}")
def read_venda(venda_id: int, session: Annotated[Session, Depends(get_session)]) -> VendaPublic:
    venda = session.get(Venda, venda_id)
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada.")
    return venda


@app.post("/venda")
def cadastrar_venda(
    venda: VendaCreate, items: list[ItemCreate], session: Annotated[Session, Depends(get_session)]
) -> VendaPublic:
    db_venda = Venda.model_validate(venda)
    db_items = [Item.model_validate(item) for item in items]
    db_venda.items = db_items
    session.add(db_venda)
    session.commit()
    session.refresh(db_venda)
    return db_venda
