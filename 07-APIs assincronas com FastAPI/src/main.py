from fastapi import FastAPI
from src.config import settings
from src.database import engine, Base
from src.controllers.account import router as account_router
from src.controllers.transaction import router as transaction_router

app = FastAPI(
    title="API Bancária Assíncrona",
    description="API para gerenciamento de contas correntes e transações com autenticação JWT",
    version="1.0.0"
)

# Inclui os routers
app.include_router(account_router, prefix="/accounts", tags=["Contas"])
app.include_router(transaction_router, prefix="/transactions", tags=["Transações"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API Bancária Assíncrona com FastAPI!"}
