from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.dependencies import get_session
from app.models import (
    Fornecedor,
    FornecedorCreate,
    FornecedorPublic,
)

router = APIRouter(prefix="/fornecedores", tags=["fornecedores"])


@router.get("/")
def read_fornecedores(session: Annotated[Session, Depends(get_session)]) -> list[FornecedorPublic]:
    fornecedores = session.exec(select(Fornecedor)).all()
    return fornecedores


@router.get("/{fornecedor_id}")
def read_fornecedor(fornecedor_id: int, session: Annotated[Session, Depends(get_session)]) -> FornecedorPublic:
    fornecedor = session.get(Fornecedor, fornecedor_id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado.")
    return fornecedor


@router.post("/")
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


@router.delete("/{fornecedor_id}")
def delete_fornecedor(fornecedor_id: int, session: Annotated[Session, Depends(get_session)]) -> FornecedorPublic:
    fornecedor = session.get(Fornecedor, fornecedor_id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado.")
    session.delete(fornecedor)
    session.commit()
    return fornecedor
