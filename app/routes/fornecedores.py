
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from app.dependencies import SessionDep
from app.models import (
    Fornecedor,
    FornecedorCreate,
    FornecedorPublic,
)

router = APIRouter(prefix="/fornecedores", tags=["fornecedores"])


@router.get("")
def read_fornecedores(session: SessionDep) -> list[FornecedorPublic]:
    fornecedores = session.exec(select(Fornecedor)).all()
    return fornecedores


@router.get("/{fornecedor_id}")
def read_fornecedor(fornecedor_id: int, session: SessionDep) -> FornecedorPublic:
    fornecedor = session.get(Fornecedor, fornecedor_id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado.")
    return fornecedor


@router.post("/")
def cadastrar_fornecedor(
    fornecedor: FornecedorCreate, session: SessionDep
) -> FornecedorPublic:
    db_fornecedor = Fornecedor.model_validate(fornecedor)
    try:
        session.add(db_fornecedor)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Já existe um fornecedor com esse nome.")
    session.refresh(db_fornecedor)
    return db_fornecedor


@router.delete("/{fornecedor_id}")
def delete_fornecedor(fornecedor_id: int, session: SessionDep) -> FornecedorPublic:
    fornecedor = session.get(Fornecedor, fornecedor_id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado.")
    session.delete(fornecedor)
    session.commit()
    return fornecedor
