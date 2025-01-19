from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy_utils import database_exists

from app.database import engine, init_database
from app.routes import clientes, compras, fornecedores, produtos, vendas

if not database_exists(engine.url):
    init_database()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes.router)
app.include_router(compras.router)
app.include_router(fornecedores.router)
app.include_router(produtos.router)
app.include_router(vendas.router)
