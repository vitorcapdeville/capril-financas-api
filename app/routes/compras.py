from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.dependencies import SessionDep
from app.models import (
    Compra,
    CompraCreate,
    CompraPublic,
    ComprasPublic,
)

router = APIRouter(prefix="/compras", tags=["compras"])


@router.get("", operation_id="read_compras")
def read_compras(session: SessionDep, query: str | None = None, skip: int = 0, limit: int = 10) -> ComprasPublic:
    count_statement = select(func.count()).select_from(Compra)
    statement = select(Compra)
    if query:
        where_expression = Compra.categoria.like(f"%{query}%")
        statement = statement.where(where_expression)
        count_statement = count_statement.where(where_expression)
    statement = statement.order_by(Compra.id).offset(skip).limit(limit)
    data = session.exec(statement).all()
    count = session.exec(count_statement).one()
    return ComprasPublic(data=data, count=count)


@router.get("/{compra_id}", operation_id="read_compra_by_id")
def read_compra(compra_id: int, session: SessionDep) -> CompraPublic:
    compra = session.get(Compra, compra_id)
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
