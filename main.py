from fastapi import FastAPI
from app.databases.database import engine, Base
from app.controllers.controller import router as hotel_router

# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

descricao_api = """
## Sistema de Gestão de Reservas de Hoteis 🏨

Esta API permite gerenciar todo o ciclo de vida de uma reserva de hotel.

### Funcionalidades:
* **Hotéis**: Cadastro e busca de hotéis e quartos.
* **Clientes**: Gestão de hóspedes.
* **Reservas**: Criação e controle de check-in/out.
* **Pagamentos**: Registro de transações financeiras.
"""

# 2. Configure os metadados das TAGS (para organizar as rotas)
tags_metadata = [
    {
        "name": "Hotéis",
        "description": "Gerenciamento de hotéis e suas informações.",
    },
    {
        "name": "Reservas",
        "description": "Fluxo de reservas e verificação de disponibilidade.",
    },
    {
        "name": "Clientes",
        "description": "Cadastro e atualização de dados dos hóspedes.",
    },
]

# 3. Injete tudo isso no FastAPI
app = FastAPI(
    title="API Hoteis - AV2 Claudiane 🏖️",
    description=descricao_api,
    version="0.1.4",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Link diretório GitHub",
        "url": "https://github.com/andreluiz05/sistema_busca_hotel",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata # <--- Liga as descrições às tags
)

# Inclui as rotas que definimos no controller
app.include_router(hotel_router)