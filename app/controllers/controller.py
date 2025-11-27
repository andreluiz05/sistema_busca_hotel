from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.databases.database import get_db
from app.models.models import HotelDB, HotelCreate, AcomodacaoCreate, AcomodacaoDB, HotelUpdate
from app.services.services import HotelService, AcomodacaoService

router = APIRouter()
service = HotelService() # Instancia a camada de serviço
acomodacaoservice = AcomodacaoService() # Instancia a camada de serviço para acomodação

@router.post("/hoteis/criar/") # Requisito POST
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

@router.get("/hoteis/{hotel_id}") # Requisito GET por ID
def obter_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.query(HotelDB).filter(HotelDB.id == hotel_id).first()
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel não encontrado")
    return hotel

@router.delete("/hoteis/{hotel_id}") # Requisito DELETE
def deletar_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.query(HotelDB).filter(HotelDB.id == hotel_id).first()
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel não encontrado")
    db.delete(hotel)
    db.commit()
    return {"detail": "Hotel deletado com sucesso"}

@router.put("/hoteis/{hotel_id}") # Requisito PUT
def atualizar_hotel(hotel_id: int, hotel_atualizado: HotelCreate, db: Session = Depends(get_db)):
    hotel = db.query(HotelDB).filter(HotelDB.id == hotel_id).first()
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel não encontrado")
    
    # Atualiza os campos
    hotel.nome = hotel_atualizado.nome
    hotel.estrelas = hotel_atualizado.estrelas
    hotel.cidade = hotel_atualizado.cidade
    hotel.preco_diaria = hotel_atualizado.preco_diaria
    hotel.estado = hotel_atualizado.estado
    hotel.endereco = hotel_atualizado.endereco
    hotel.cep = hotel_atualizado.cep
    hotel.responsavel = hotel_atualizado.responsavel
    hotel.telefone = hotel_atualizado.telefone

    db.commit()
    db.refresh(hotel)
    return hotel

@router.get("/hoteis/cidade/{cidade}") # Requisito GET por cidade
def listar_hoteis_por_cidade(cidade: str, db: Session = Depends(get_db)):
    hoteis = db.query(HotelDB).filter(HotelDB.cidade == cidade).all()
    return hoteis  

@router.get("/hoteis/estrelas/{min_estrelas}") # Requisito GET por estrelas mínimas
def listar_hoteis_por_estrelas(min_estrelas: int, db: Session       = Depends(get_db)):
    hoteis = db.query(HotelDB).filter(HotelDB.estrelas >= min_estrelas).all()
    return hoteis

@router.get("/hoteis/preco/{max_preco}") # Requisito GET por preço máximo
def listar_hoteis_por_preco(max_preco: float, db: Session = Depends     (get_db)):
    hoteis = db.query(HotelDB).filter(HotelDB.preco_diaria <= max_preco).all()
    return hoteis

@router.get("/hoteis/filtro/") # Requisito GET com múltiplos filtros
def listar_hoteis_com_filtros(
    cidade: str = None,
    min_estrelas: int = None,
    max_preco: float = None,
    db: Session = Depends(get_db)
):
    query = db.query(HotelDB)
    
    if cidade:
        query = query.filter(HotelDB.cidade == cidade)
    if min_estrelas:
        query = query.filter(HotelDB.estrelas >= min_estrelas)
    if max_preco:
        query = query.filter(HotelDB.preco_diaria <= max_preco)
    
    hoteis = query.all()
    return hoteis

@router.patch("/hoteis/atualizar/{hotel_id}") # Requisito PATCH
def atualizar_parcial_hotel(hotel_id: int, hotel_atualizado: HotelUpdate, db: Session = Depends(get_db)):
    hotel = db.query(HotelDB).filter(HotelDB.id == hotel_id).first()
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel não encontrado")
    
    # Atualiza apenas os campos fornecidos
    if hotel_atualizado.nome is not None:
        hotel.nome = hotel_atualizado.nome
    if hotel_atualizado.estrelas is not None:
        hotel.estrelas = hotel_atualizado.estrelas
    if hotel_atualizado.cidade is not None:
        hotel.cidade = hotel_atualizado.cidade
    if hotel_atualizado.preco_diaria is not None:
        hotel.preco_diaria = hotel_atualizado.preco_diaria
    if hotel_atualizado.estado is not None:
        hotel.estado = hotel_atualizado.estado
    if hotel_atualizado.cidade is not None:
        hotel.cidade = hotel_atualizado.cidade
    if hotel_atualizado.endereco is not None:
        hotel.endereco = hotel_atualizado.endereco
    if hotel_atualizado.cep is not None:
        hotel.cep = hotel_atualizado.cep
    if hotel_atualizado.responsavel is not None:
        hotel.responsavel = hotel_atualizado.responsavel
    if hotel_atualizado.telefone is not None:
        hotel.telefone = hotel_atualizado.telefone

    db.commit()
    db.refresh(hotel)
    return hotel

@router.post("/acomodacoes/criar/") # Requisito POST para acomodação
def cadastrar_acomodacao(acomodacao: AcomodacaoCreate, db: Session = Depends(get_db)):
    try:
        # Chama o service para resolver
        novo_acomodacao = acomodacaoservice.criar_acomodacao(db, acomodacao)
        return novo_acomodacao
    except Exception as e:
        # Captura o erro da regra de negócio
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/acomodacoes/") # Requisito GET para listar acomodações
def listar_acomodacoes(db: Session = Depends(get_db)):
    return db.query(AcomodacaoDB).all() 

@router.get("/acomodacoes/{acomodacao_id}") # Requisito GET por ID de acomodação
def obter_acomodacao(acomodacao_id: int, db: Session = Depends(get_db)):
    acomodacao = db.query(AcomodacaoDB).filter(AcomodacaoDB.id == acomodacao_id).first()
    if acomodacao is None:
        raise HTTPException(status_code=404, detail="Acomodação não encontrada")
    return acomodacao

@router.get("/hoteis/{hotel_id}/acomodacoes/") # Requisito GET para listar acomodações de um hotel
def listar_acomodacoes_por_hotel(hotel_id: int, db: Session = Depends(get_db)):
    acomodacoes = db.query(AcomodacaoDB).filter(AcomodacaoDB.hotel_id == hotel_id).all()
    return acomodacoes