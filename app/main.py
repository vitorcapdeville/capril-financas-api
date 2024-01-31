from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy_utils import database_exists
from sqlmodel import Session, select

from .database import create_tables, engine
from .dependencies import get_session
from .models import Fornecedor, Insumo

if not database_exists(engine.url):
    create_tables()

app = FastAPI()


@app.get("/")
def root():
    return "Server is running."


@app.get("/fornecedores")
def read_fornecedores(
    session: Annotated[Session, Depends(get_session)]
) -> list[Fornecedor]:
    fornecedores = session.exec(select(Fornecedor)).all()
    return fornecedores


@app.post("/fornecedor")
def cadastrar_fornecedor(
    fornecedor: Fornecedor, session: Annotated[Session, Depends(get_session)]
) -> Fornecedor:
    session.add(fornecedor)
    session.commit()
    session.refresh(fornecedor)
    return fornecedor


@app.post("/insumo")
def adicionar_insumo(
    insumo: Insumo, session: Annotated[Session, Depends(get_session)]
) -> Insumo:
    session.add(insumo)
    session.commit()
    session.refresh(insumo)
    return insumo

@app.delete("/fornecedor/{nome}")
def delete_fornecedor(nome: str):
    with Session(engine) as session:
        nome = session.get(Fornecedor, nome)
        if not nome:
            raise HTTPException(status_code=404, detail= "Esse nome não foi encontrado.")
        session.delete(nome)
        session.commit()
        return {"ok": True}
    
@app.delete("/insumo/{nome}")
def delete_insumo(insumo: str):
    with Session(engine) as session:
        insumo = session.get(Insumo, insumo)
        if not insumo:
            raise HTTPException(status_code=404, detail= "Esse nome não foi encontrado.")
        session.delete(insumo)
        session.commit()
        return {"ok": True}
