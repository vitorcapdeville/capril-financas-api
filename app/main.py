from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy_utils import database_exists
from sqlmodel import Session

from app.core.config import settings
from app.core.db import engine, init_db
from app.routes import clientes, compras, fornecedores, login, produtos, vendas

if not database_exists(engine.url):
    with Session(engine) as session:
        init_db(session)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(clientes.router)
app.include_router(compras.router)
app.include_router(fornecedores.router)
app.include_router(produtos.router)
app.include_router(vendas.router)
app.include_router(login.router)
