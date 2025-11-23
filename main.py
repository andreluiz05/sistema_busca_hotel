from fastapi import FastAPI
from app.databases.database import engine, Base
from app.controllers.controller import router as hotel_router

# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Inclui as rotas que definimos no controller
app.include_router(hotel_router)