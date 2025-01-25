from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import func, select

from app.dependencies import SessionDep
from app.models import Cliente, ClienteCreate, ClientePublic, ClientesPublic

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("", operation_id="read_clientes")
def read_clientes(session: SessionDep, query: str | None = None, skip: int = 0, limit: int = 10) -> ClientesPublic:
    count_statement = select(func.count()).select_from(Cliente)
    statement = select(Cliente)
    if query:
        where_expression = Cliente.nome.like(f"%{query}%")
        statement = statement.where(where_expression)
        count_statement = count_statement.where(where_expression)
    statement = statement.order_by(Cliente.id).offset(skip).limit(limit)
    data = session.exec(statement).all()
    count = session.exec(count_statement).one()
    return ClientesPublic(data=data, count=count)


@router.get("/{id}", operation_id="read_cliente_by_id")
def read_cliente(id: int, session: SessionDep) -> ClientePublic:
    cliente = session.get(Cliente, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return cliente


@router.post("", operation_id="create_cliente")
def cadastrar_cliente(cliente: ClienteCreate, session: SessionDep) -> ClientePublic:
    db_cliente = Cliente.model_validate(cliente)
    try:
        session.add(db_cliente)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Já existe um cliente com esse nome.")
    session.refresh(db_cliente)
    return db_cliente


@router.delete("/{id}", operation_id="delete_cliente")
def delete_cliente(id: int, session: SessionDep) -> ClientePublic:
    cliente = session.get(Cliente, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    session.delete(cliente)
    session.commit()
    return cliente
