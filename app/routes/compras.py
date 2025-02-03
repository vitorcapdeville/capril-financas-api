from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import func, select

from app.dependencies import SessionDep
from app.models import (
    Compra,
    CompraCreate,
    CompraPublic,
)

router = APIRouter(prefix="/compras", tags=["compras"])


@router.get("", operation_id="read_compras")
def read_compras(session: SessionDep, query: str | None = None, skip: int = 0, limit: int = 10) -> list[CompraPublic]:
    statement = select(Compra)
    if query:
        where_expression = Compra.categoria.like(f"%{query}%")
        statement = statement.where(where_expression)
    statement = statement.order_by(Compra.id).offset(skip).limit(limit)
    data = session.exec(statement).all()
    return data


@router.get("/count", operation_id="count_compras")
def count_compras(session: SessionDep, query: str | None = None) -> int:
    count_statement = select(func.count()).select_from(Compra)
    if query:
        where_expression = Compra.categoria.like(f"%{query}%")
        count_statement = count_statement.where(where_expression)
    count = session.exec(count_statement).one()
    return count


@router.get("/{id}", operation_id="read_compra_by_id")
def read_compra(id: int, session: SessionDep) -> CompraPublic:
    compra = session.get(Compra, id)
    if not compra:
        raise HTTPException(status_code=404, detail="Compra não encontrada.")
    return compra


@router.post("", operation_id="create_compra")
def cadastrar_compra(compra: CompraCreate, session: SessionDep) -> CompraPublic:
    db_compra = Compra.model_validate(compra)
    session.add(db_compra)
    session.commit()
    session.refresh(db_compra)
    return db_compra


@router.delete("/{id}", operation_id="delete_compra")
def delete_compra(id: int, session: SessionDep):
    compra = session.get(Compra, id)
    if not compra:
        raise HTTPException(status_code=404, detail="Compra não encontrado.")
    compra.fornecedor = None
    try:
        session.delete(compra)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Não é possível deletar essa compra.")
