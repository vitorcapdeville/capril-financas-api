from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.dependencies import get_session
from app.models import (
    Produto,
    ProdutoCreate,
    ProdutoPublic,
)

router = APIRouter(prefix="/produtos", tags=["produtos"])


@router.get("/")
def read_produtos(session: Annotated[Session, Depends(get_session)]) -> list[ProdutoPublic]:
    produtos = session.exec(select(Produto)).all()
    return produtos


@router.get("/{produto_id}")
def read_produto(produto_id: int, session: Annotated[Session, Depends(get_session)]) -> ProdutoPublic:
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return produto


@router.post("/")
def cadastrar_produto(produto: ProdutoCreate, session: Annotated[Session, Depends(get_session)]) -> ProdutoPublic:
    db_produto = Produto.model_validate(produto)
    try:
        session.add(db_produto)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Já existe um produto com esse nome.")
    session.refresh(db_produto)
    return db_produto


@router.delete("/{produto_id}")
def delete_produto(produto_id: int, session: Annotated[Session, Depends(get_session)]) -> ProdutoPublic:
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    session.delete(produto)
    session.commit()
    return produto
