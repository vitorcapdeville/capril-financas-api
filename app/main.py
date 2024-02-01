from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy_utils import database_exists
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from .database import create_tables, engine
from .dependencies import get_session
from .models import Fornecedor, Insumo

if not database_exists(engine.url):
    create_tables()

app = FastAPI()

origins = [
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    try:
        session.add(fornecedor)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code= 409, detail= "Já existe um fornecedor com esse nome.") 
    session.refresh(fornecedor)
    return fornecedor


@app.post("/insumo")
def adicionar_insumo(
    insumo: Insumo, session: Annotated[Session, Depends(get_session)]
) -> Insumo:
    try:
        session.add(insumo)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code= 409, detail= "Já existe um insumo com esse nome.")
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
