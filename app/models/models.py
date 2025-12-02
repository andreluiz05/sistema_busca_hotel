from sqlalchemy import Column, Integer, String, Float, ForeignKey,Date
from sqlalchemy.orm import relationship
from app.databases.database import Base

# --- SQLAlchemy (Para salvar no banco) ---
class HotelDB(Base):
    __tablename__ = "hoteis"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(200))
    estrelas = Column(Integer)
    cidade = Column(String(200))
    preco_diaria = Column(Float)
    estado = Column(String(2))
    endereco = Column(String(200))
    cep = Column(String(200))
    responsavel = Column(String(200))
    telefone = Column(String(200))
    acomodacoes = relationship("AcomodacaoDB", back_populates="hotel")
    
class AcomodacaoDB(Base):
    __tablename__ = "acomodacoes"
    
    id = Column(Integer, primary_key=True)
    tipo = Column(String(50))
    capacidade = Column(Integer)
    preco_noite = Column(Float)
    hotel_id = Column(Integer, ForeignKey("hoteis.id"))  # Foreign key para a tabela hotel
    hotel = relationship("HotelDB", back_populates="acomodacoes")
    datas_reservadas = relationship("ReservaDB", back_populates="acomodacao")

class ClienteDB(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(200))
    email = Column(String(200), unique=True, index=True)
    telefone = Column(String(200))
    cpf = Column(String(200), unique=True, index=True)
    birthdate = Column(Date)
    reservas = relationship("ReservaDB", back_populates="cliente")

class ReservaDB(Base):
    __tablename__ = "reservas"
    
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    acomodacao_id = Column(Integer, ForeignKey("acomodacoes.id"))
    data_checkin = Column(String(200))
    data_checkout = Column(String(200))
    cliente = relationship("ClienteDB", back_populates="reservas")
    acomodacao = relationship("AcomodacaoDB")
    last_payment = relationship("PagamentoDB", uselist=False, back_populates="reserva")
    last_update = Column(String(200))

class PagamentoDB(Base):
    __tablename__ = "pagamentos"
    
    id = Column(Integer, primary_key=True)
    reserva_id = Column(Integer, ForeignKey("reservas.id"))
    valor = Column(Float)
    data_pagamento = Column(Date)
    hora_pagamento = Column(String(200))
    metodo_pagamento = Column(String(200))
    codigo_transacao = Column(String(200))
    reserva = relationship("ReservaDB")

class FeedbackDB(Base):
    __tablename__ = "feedbacks"
    
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    hotel_id = Column(Integer, ForeignKey("hoteis.id"))
    avaliacao = Column(Integer)
    comentario = Column(String(200))
    cliente = relationship("ClienteDB")
    hotel = relationship("HotelDB")
    
# class CargoFuncionarioDB(Base):
#     __tablename__ = "cargos_funcionarios"
    
#     id = Column(Integer, primary_key=True, index=True)
#     nome_cargo = Column(String(20), unique=True, index=True)
#     descricao = Column(String(255))
    
# class FuncionarioDB(Base):
#     __tablename__ = "funcionarios"
    
#     id = Column(Integer, primary_key=True)
#     nome = Column(String)
#     email = Column(String, unique=True, index=True)
#     telefone = Column(String)
#     cargo_id = Column(Integer, ForeignKey("cargos_funcionarios.id"))
#     cargo = relationship("CargoFuncionarioDB")