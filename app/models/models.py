from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.databases.database import Base
from pydantic import BaseModel
from typing import Optional

# --- Pydantic (Para receber dados do usuário) ---
class HotelCreate(BaseModel):
    nome: str
    estrelas: int
    cidade: str
    preco_diaria: float
    estado: str
    endereco: str
    cep: str
    responsavel: str
    telefone: str

class AcomodacaoCreate(BaseModel):
    tipo: str
    capacidade: int
    preco_noite: float
    hotel_id: int

class HotelUpdate(BaseModel):
    nome: Optional[str] = None
    estrelas: Optional[int] = None
    cidade: Optional[str] = None
    preco_diaria: Optional[float] = None
    estado: Optional[str] = None
    endereco: Optional[str] = None
    cep: Optional[str] = None
    responsavel: Optional[str] = None
    telefone: Optional[str] = None

# --- SQLAlchemy (Para salvar no banco) ---
class HotelDB(Base):
    __tablename__ = "hoteis"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    estrelas = Column(Integer)
    cidade = Column(String)
    preco_diaria = Column(Float)
    estado = Column(String)
    endereco = Column(String)
    cep = Column(String)
    responsavel = Column(String)
    telefone = Column(String)
    acomodacoes = relationship("AcomodacaoDB", back_populates="hotel")
    
class AcomodacaoDB(Base):
    __tablename__ = "acomodacoes"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String)
    capacidade = Column(Integer)
    preco_noite = Column(Float)
    hotel_id = Column(Integer, ForeignKey("hoteis.id"))  # Foreign key para a tabela hotel
    hotel = relationship("HotelDB", back_populates="acomodacoes")