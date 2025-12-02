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