from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.dependencies import SessionDep
from app.models import Item, ItemCreate, Venda, VendaCreate, VendaPublic

router = APIRouter(prefix="/vendas", tags=["vendas"])


@router.get("/")
def read_vendas(session: SessionDep) -> list[VendaPublic]:
    vendas = session.exec(select(Venda)).all()
    return vendas


@router.get("/{venda_id}")
def read_venda(venda_id: int, session: SessionDep) -> VendaPublic:
    venda = session.get(Venda, venda_id)
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada.")
    return venda


@router.post("/")
def cadastrar_venda(venda: VendaCreate, items: list[ItemCreate], session: SessionDep) -> VendaPublic:
    db_venda = Venda.model_validate(venda)
    db_items = [Item.model_validate(item) for item in items]
    db_venda.items = db_items
    session.add(db_venda)
    session.commit()
    session.refresh(db_venda)
    return db_venda
