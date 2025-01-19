from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from app.dependencies import SessionDep
from app.models import (
    Cliente,
    ClienteCreate,
    ClientePublic,
)

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("")
def read_clientes(session: SessionDep) -> list[ClientePublic]:
    clientes = session.exec(select(Cliente)).all()
    return clientes


@router.get("/{cliente_id}")
def read_cliente(cliente_id: int, session: SessionDep) -> ClientePublic:
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return cliente


@router.post("/")
def cadastrar_cliente(cliente: ClienteCreate, session: SessionDep) -> ClientePublic:
    db_cliente = Cliente.model_validate(cliente)
    try:
        session.add(db_cliente)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Já existe um cliente com esse nome.")
    session.refresh(db_cliente)
    return db_cliente


@router.delete("/{cliente_id}")
def delete_cliente(cliente_id: int, session: SessionDep) -> ClientePublic:
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    session.delete(cliente)
    session.commit()
    return cliente
