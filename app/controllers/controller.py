from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.databases.database import get_db
from app.models.models import HotelCreate
from app.services.services import HotelService

router = APIRouter()
service = HotelService() # Instancia a camada de serviço

@router.post("/hoteis/") # Requisito POST
def cadastrar_hotel(hotel: HotelCreate, db: Session = Depends(get_db)):
    try:
        # Chama o service para resolver
        novo_hotel = service.criar_hotel(db, hotel)
        return novo_hotel
    except Exception as e:
        # Captura o erro da regra de negócio
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/hoteis/") # Requisito GET
def listar_hoteis(db: Session = Depends(get_db)):
    return service.listar_hoteis(db)

