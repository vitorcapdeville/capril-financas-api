from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy_utils import database_exists
from sqlmodel import Session

from .database import create_tables, engine
from .dependencies import get_session
from .models import Fornecedor

if not database_exists(engine.url):
    create_tables()

app = FastAPI()


@app.get("/")
def root():
    return "Server is running."


@app.post("/fornecedor")
def cadastrar_fornecedor(
    fornecedor: Fornecedor, session: Annotated[Session, Depends(get_session)]
) -> Fornecedor:
    session.add(fornecedor)
    session.commit()
    session.refresh(fornecedor)
    return fornecedor
