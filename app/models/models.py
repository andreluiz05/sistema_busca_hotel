from sqlalchemy import Column, Integer, String, Float
from app.databases.database import Base
from pydantic import BaseModel

# --- Pydantic (Para receber dados do usuário) ---
class HotelCreate(BaseModel):
    nome: str
    estrelas: int
    cidade: str
    preco_diaria: float

# --- SQLAlchemy (Para salvar no banco) ---
# DICA POO: Que tal criar uma classe "AcomodacaoBase" primeiro?
class HotelDB(Base):
    __tablename__ = "hoteis"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    estrelas = Column(Integer)
    cidade = Column(String)
    # ... adicione os outros campos aqui