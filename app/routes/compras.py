from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.dependencies import get_session
from app.models import (
    Compra,
    CompraCreate,
    CompraPublic,
)

router = APIRouter(prefix="/compras", tags=["compras"])


@router.get("/")
def read_compras(session: Annotated[Session, Depends(get_session)]) -> list[CompraPublic]:
    compras = session.exec(select(Compra)).all()
    return compras


@router.get("/{compra_id}")
def read_compra(compra_id: int, session: Annotated[Session, Depends(get_session)]) -> CompraPublic:
    compra = session.get(Compra, compra_id)
    if not compra:
        raise HTTPException(status_code=404, detail="Compra não encontrada.")
    return compra


@router.post("/")
def cadastrar_compra(compra: CompraCreate, session: Annotated[Session, Depends(get_session)]) -> CompraPublic:
    db_compra = Compra.model_validate(compra)
    session.add(db_compra)
    session.commit()
    session.refresh(db_compra)
    return db_compra
