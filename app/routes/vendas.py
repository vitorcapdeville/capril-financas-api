from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.dependencies import SessionDep
from app.models import Item, Venda, VendaCreate, VendaPublic

router = APIRouter(prefix="/vendas", tags=["vendas"])


@router.get("", operation_id="read_vendas")
def read_vendas(session: SessionDep, query: str | None = None, skip: int = 0, limit: int = 10) -> list[VendaPublic]:
    statement = select(Venda)
    if query:
        where_expression = Venda.id.like(f"%{query}%")
        statement = statement.where(where_expression)
    statement = statement.order_by(Venda.id).offset(skip).limit(limit)
    data = session.exec(statement).all()
    return data


@router.get("/count", operation_id="count_vendas")
def count_vendas(session: SessionDep, query: str | None = None) -> int:
    count_statement = select(func.count()).select_from(Venda)
    if query:
        where_expression = Venda.id.like(f"%{query}%")
        count_statement = count_statement.where(where_expression)
    count = session.exec(count_statement).one()
    return count


@router.get("/{id}", operation_id="read_venda_by_id")
def read_venda(id: int, session: SessionDep) -> VendaPublic:
    venda = session.get(Venda, id)
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada.")
    return venda


@router.post("", operation_id="create_venda")
def cadastrar_venda(venda: VendaCreate, session: SessionDep) -> VendaPublic:
    db_items = [Item.model_validate(item) for item in venda.items]
    venda.items = db_items
    db_venda = Venda.model_validate(venda)
    session.add(db_venda)
    session.commit()
    session.refresh(db_venda)
    return db_venda
