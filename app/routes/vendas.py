from fastapi import APIRouter, HTTPException
from sqlmodel import select, func

from app.dependencies import SessionDep
from app.models import Item, ItemCreate, Venda, VendaCreate, VendaPublic, VendasPublic

router = APIRouter(prefix="/vendas", tags=["vendas"])


@router.get("", operation_id="read_vendas")
def read_vendas(session: SessionDep, query: str | None = None, skip: int = 0, limit: int = 10) -> VendasPublic:
    count_statement = select(func.count()).select_from(Venda)
    statement = select(Venda)
    if query:
        where_expression = Venda.id.like(f"%{query}%")
        statement = statement.where(where_expression)
        count_statement = count_statement.where(where_expression)
    statement = statement.order_by(Venda.id).offset(skip).limit(limit)
    data = session.exec(statement).all()
    count = session.exec(count_statement).one()
    return VendasPublic(data=data, count=count)


@router.get("/{venda_id}", operation_id="read_venda_by_id")
def read_venda(venda_id: int, session: SessionDep) -> VendaPublic:
    venda = session.get(Venda, venda_id)
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada.")
    return venda


@router.post("", operation_id="create_venda")
def cadastrar_venda(venda: VendaCreate, items: list[ItemCreate], session: SessionDep) -> VendaPublic:
    db_venda = Venda.model_validate(venda)
    db_items = [Item.model_validate(item) for item in items]
    db_venda.items = db_items
    session.add(db_venda)
    session.commit()
    session.refresh(db_venda)
    return db_venda
