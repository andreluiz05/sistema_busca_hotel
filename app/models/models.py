from sqlalchemy import Column, Integer, String, Float, ForeignKey,Date
from sqlalchemy.orm import relationship
from app.databases.database import Base
from pydantic import BaseModel
from datetime import date
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

class AcomodacaoUpdate(BaseModel):
    tipo: Optional[str] = None
    capacidade: Optional[int] = None
    preco_noite: Optional[float] = None
    hotel_id: Optional[int] = None
    
# Cliente Pydantic Models
class ClienteCreate(BaseModel):
    nome: str
    email: str
    telefone: str
    cpf: str
    birthdate: date

class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    cpf: Optional[str] = None
    birthdate: Optional[date] = None
    
# Reserva Pydantic Models

class ReservaCreate(BaseModel):
    cliente_id: int
    acomodacao_id: int
    data_checkin: str
    data_checkout: str
    
# Pagamento Pydantic Models

class PagamentoCreate(BaseModel):
    valor: float
    data_pagamento: date
    hora_pagamento: str
    metodo_pagamento: str
    codigo_transacao: str

# Feedback Pydantic Models

class FeedbackCreate(BaseModel):
    cliente_id: int
    hotel_id: int
    avaliacao: int
    comentario: str
    
# # CargoFuncionario Pydantic Models 

# class CargoFuncionarioCreate(BaseModel):
#     nome_cargo: str
#     descricao: str
# # Funcionario Pydantic Models

# class FuncionarioCreate(BaseModel):
#     nome: str
#     email: str
#     telefone: str
#     cargo_id: int



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
    datas_reservadas = relationship("ReservaDB", back_populates="acomodacao")

class ClienteDB(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    telefone = Column(String)
    cpf = Column(String, unique=True, index=True)
    birthdate = Column(Date)
    reservas = relationship("ReservaDB", back_populates="cliente")

class ReservaDB(Base):
    __tablename__ = "reservas"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    acomodacao_id = Column(Integer, ForeignKey("acomodacoes.id"))
    data_checkin = Column(String)
    data_checkout = Column(String)
    cliente = relationship("ClienteDB", back_populates="reservas")
    acomodacao = relationship("AcomodacaoDB")
    last_payment = relationship("PagamentoDB", uselist=False, back_populates="reserva")
    last_update = Column(String)

class PagamentoDB(Base):
    __tablename__ = "pagamentos"
    
    id = Column(Integer, primary_key=True, index=True)
    reserva_id = Column(Integer, ForeignKey("reservas.id"))
    valor = Column(Float)
    data_pagamento = Column(Date)
    hora_pagamento = Column(String)
    metodo_pagamento = Column(String)
    codigo_transacao = Column(String)
    reserva = relationship("ReservaDB")

class FeedbackDB(Base):
    __tablename__ = "feedbacks"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    hotel_id = Column(Integer, ForeignKey("hoteis.id"))
    avaliacao = Column(Integer)
    comentario = Column(String)
    cliente = relationship("ClienteDB")
    hotel = relationship("HotelDB")
    
# class CargoFuncionarioDB(Base):
#     __tablename__ = "cargos_funcionarios"
    
#     id = Column(Integer, primary_key=True, index=True)
#     nome_cargo = Column(String)
#     descricao = Column(String)
    
# class FuncionarioDB(Base):
#     __tablename__ = "funcionarios"
    
#     id = Column(Integer, primary_key=True, index=True)
#     nome = Column(String)
#     email = Column(String, unique=True, index=True)
#     telefone = Column(String)
#     cargo_id = Column(Integer, ForeignKey("cargos_funcionarios.id"))
#     cargo = relationship("CargoFuncionarioDB")