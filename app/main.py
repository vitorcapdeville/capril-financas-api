import asyncio
import time

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.status import HTTP_504_GATEWAY_TIMEOUT

from app.core.config import settings
from app.dependencies import get_current_user
from app.routes import clientes, compras, fornecedores, login, produtos, vendas

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]


@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    try:
        start_time = time.time()
        return await asyncio.wait_for(call_next(request), timeout=8)

    except asyncio.TimeoutError:
        process_time = time.time() - start_time
        return JSONResponse(
            {
                "detail": "Tempo limite de processamento atingido. Por favor, tente novamente.",
                "processing_time": process_time,
            },
            status_code=HTTP_504_GATEWAY_TIMEOUT,
        )


# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(clientes.router, dependencies=[Depends(get_current_user)])
app.include_router(compras.router, dependencies=[Depends(get_current_user)])
app.include_router(fornecedores.router, dependencies=[Depends(get_current_user)])
app.include_router(produtos.router, dependencies=[Depends(get_current_user)])
app.include_router(vendas.router, dependencies=[Depends(get_current_user)])
app.include_router(login.router)
