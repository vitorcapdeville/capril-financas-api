from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import func, select

from app.dependencies import SessionDep
from app.models import (
    Fornecedor,
    FornecedorCreate,
    FornecedorPublic,
    FornecedoresPublic,
)

router = APIRouter(prefix="/fornecedores", tags=["fornecedores"])


@router.get("", operation_id="read_fornecedores")
def read_fornecedores(
    session: SessionDep, query: str | None = None, skip: int = 0, limit: int = 10
) -> FornecedoresPublic:
    count_statement = select(func.count()).select_from(Fornecedor)
    statement = select(Fornecedor)
    if query:
        where_expression = Fornecedor.nome.like(f"%{query}%")
        statement = statement.where(where_expression)
        count_statement = count_statement.where(where_expression)
    statement = statement.order_by(Fornecedor.id).offset(skip).limit(limit)
    data = session.exec(statement).all()
    count = session.exec(count_statement).one()
    return FornecedoresPublic(data=data, count=count)


@router.get("/{id}", operation_id="read_fornecedor_by_id")
def read_fornecedor(id: int, session: SessionDep) -> FornecedorPublic:
    fornecedor = session.get(Fornecedor, id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado.")
    return fornecedor


@router.post("", operation_id="create_fornecedor")
def cadastrar_fornecedor(fornecedor: FornecedorCreate, session: SessionDep) -> FornecedorPublic:
    db_fornecedor = Fornecedor.model_validate(fornecedor)
    try:
        session.add(db_fornecedor)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Já existe um fornecedor com esse nome.")
    session.refresh(db_fornecedor)
    return db_fornecedor


@router.delete("/{id}", operation_id="delete_fornecedor")
def delete_fornecedor(id: int, session: SessionDep) -> FornecedorPublic:
    fornecedor = session.get(Fornecedor, id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado.")
    session.delete(fornecedor)
    session.commit()
    return fornecedor
