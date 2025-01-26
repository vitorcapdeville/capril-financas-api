from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import func, select

from app.dependencies import SessionDep
from app.models import Produto, ProdutoCreate, ProdutoPublic

router = APIRouter(prefix="/produtos", tags=["produtos"])


@router.get("", operation_id="read_produtos")
def read_produtos(session: SessionDep, query: str | None = None, skip: int = 0, limit: int = 10) -> list[ProdutoPublic]:
    statement = select(Produto)
    if query:
        where_expression = Produto.nome.like(f"%{query}%")
        statement = statement.where(where_expression)
    statement = statement.order_by(Produto.id).offset(skip).limit(limit)
    data = session.exec(statement).all()
    return data


@router.get("/count", operation_id="count_produtos")
def count_produtos(session: SessionDep, query: str | None = None) -> int:
    count_statement = select(func.count()).select_from(Produto)
    if query:
        where_expression = Produto.nome.like(f"%{query}%")
        count_statement = count_statement.where(where_expression)
    count = session.exec(count_statement).one()
    return count


@router.get("/{id}", operation_id="read_produto_by_id")
def read_produto(id: int, session: SessionDep) -> ProdutoPublic:
    produto = session.get(Produto, id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return produto


@router.post("", operation_id="create_produto")
def cadastrar_produto(produto: ProdutoCreate, session: SessionDep) -> ProdutoPublic:
    db_produto = Produto.model_validate(produto)
    try:
        session.add(db_produto)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Já existe um produto com esse nome.")
    session.refresh(db_produto)
    return db_produto


@router.delete("/{id}", operation_id="delete_produto")
def delete_produto(id: int, session: SessionDep) -> ProdutoPublic:
    produto = session.get(Produto, id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    session.delete(produto)
    session.commit()
    return produto
