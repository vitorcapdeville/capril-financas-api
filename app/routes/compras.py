
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.dependencies import SessionDep
from app.models import (
    Compra,
    CompraCreate,
    CompraPublic,
)

router = APIRouter(prefix="/compras", tags=["compras"])


@router.get("/")
def read_compras(session: SessionDep) -> list[CompraPublic]:
    compras = session.exec(select(Compra)).all()
    return compras


@router.get("/{compra_id}")
def read_compra(compra_id: int, session: SessionDep) -> CompraPublic:
    compra = session.get(Compra, compra_id)
    if not compra:
        raise HTTPException(status_code=404, detail="Compra não encontrada.")
    return compra


@router.post("/")
def cadastrar_compra(compra: CompraCreate, session: SessionDep) -> CompraPublic:
    db_compra = Compra.model_validate(compra)
    session.add(db_compra)
    session.commit()
    session.refresh(db_compra)
    return db_compra
