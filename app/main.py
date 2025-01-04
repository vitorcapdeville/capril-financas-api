from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import database_exists
from sqlmodel import Session, select

from .database import create_tables, engine
from .dependencies import get_session
from .models import Cliente, Fornecedor, Produto

if not database_exists(engine.url):
    create_tables()

app = FastAPI()

origins = ["http://127.0.0.1:5500"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/fornecedores")
def read_fornecedores(session: Annotated[Session, Depends(get_session)]) -> list[Fornecedor]:
    fornecedores = session.exec(select(Fornecedor)).all()
    return fornecedores


@app.post("/fornecedor")
def cadastrar_fornecedor(fornecedor: Fornecedor, session: Annotated[Session, Depends(get_session)]) -> Fornecedor:
    try:
        session.add(fornecedor)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Já existe um fornecedor com esse nome.")
    session.refresh(fornecedor)
    return fornecedor


@app.delete("/fornecedor/{fornecedor_id}")
def delete_fornecedor(fornecedor_id: int, session: Annotated[Session, Depends(get_session)]) -> Fornecedor:
    fornecedor = session.get(Fornecedor, fornecedor_id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado.")
    session.delete(fornecedor)
    session.commit()
    return fornecedor


@app.get("/produtos")
def read_produtos(session: Annotated[Session, Depends(get_session)]) -> list[Produto]:
    produtos = session.exec(select(Produto)).all()
    return produtos


@app.post("/produto")
def cadastrar_produto(produto: Produto, session: Annotated[Session, Depends(get_session)]) -> Produto:
    try:
        session.add(produto)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Já existe um produto com esse nome.")
    session.refresh(produto)
    return produto


@app.delete("/produto/{produto_id}")
def delete_produto(produto_id: int, session: Annotated[Session, Depends(get_session)]) -> Produto:
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    session.delete(produto)
    session.commit()
    return produto


@app.get("/clientes")
def read_clientes(session: Annotated[Session, Depends(get_session)]) -> list[Cliente]:
    clientes = session.exec(select(Cliente)).all()
    return clientes


@app.post("/cliente")
def cadastrar_cliente(cliente: Cliente, session: Annotated[Session, Depends(get_session)]) -> Cliente:
    try:
        session.add(cliente)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Já existe um cliente com esse nome.")
    session.refresh(cliente)
    return cliente


@app.delete("/cliente/{cliente_id}")
def delete_cliente(cliente_id: int, session: Annotated[Session, Depends(get_session)]) -> Cliente:
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    session.delete(cliente)
    session.commit()
    return cliente
