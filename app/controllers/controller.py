from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.databases.database import get_db
from app.models.models import HotelDB, ReservaDB, PagamentoDB, AcomodacaoDB, ClienteDB, FeedbackDB
from app.schemas.schema import ReservaCreate, PagamentoCreate, HotelCreate, AcomodacaoCreate, HotelUpdate, ClienteCreate, ClienteUpdate, AcomodacaoUpdate, FeedbackCreate
from app.services.services import HotelService, AcomodacaoService, ClienteService, ReservaService, PagamentoService, FeedbackService

router = APIRouter()
service = HotelService() # Instancia a camada de serviço
acomodacao_service = AcomodacaoService() # Instancia a camada de serviço para acomodação
cliente_service = ClienteService() # Instancia a camada de serviço para cliente
reserva_service = ReservaService() # Instancia a camada de serviço para reserva
pagamento_service = PagamentoService() # Instancia a camada de serviço para pagamento


@router.post("/hoteis/criar/", tags=["Hotéis"]) # Requisito POST
def cadastrar_hotel(hotel: HotelCreate, db: Session = Depends(get_db)):
    try:
        # Chama o service para resolver
        novo_hotel = service.criar_hotel(db, hotel)
        return novo_hotel
    except Exception as e:
        # Captura o erro da regra de negócio
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/hoteis/", tags=["Hotéis"]) # Requisito GET
def listar_hoteis(db: Session = Depends(get_db)):
    return service.listar_hoteis(db)

@router.get("/hoteis/{hotel_id}", tags=["Hotéis"]) # Requisito GET por ID
def obter_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.query(HotelDB).filter(HotelDB.id == hotel_id).first()
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel não encontrado")
    return hotel

@router.delete("/hoteis/{hotel_id}", tags=["Hotéis"]) # Requisito DELETE
def deletar_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.query(HotelDB).filter(HotelDB.id == hotel_id).first()
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel não encontrado")
    db.delete(hotel)
    db.commit()
    return {"detail": "Hotel deletado com sucesso"}

@router.patch("/hoteis/atualizar/{hotel_id}", tags=["Hotéis"]) # Requisito PATCH
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
   

@router.get("/hoteis/cidade/{cidade}", tags=["Hotéis"]) # Requisito GET por cidade
def listar_hoteis_por_cidade(cidade: str, db: Session = Depends(get_db)):
    hoteis = db.query(HotelDB).filter(HotelDB.cidade == cidade).all()
    return hoteis  

@router.get("/hoteis/estrelas/{min_estrelas}", tags=["Hotéis"]) # Requisito GET por estrelas mínimas
def listar_hoteis_por_estrelas(min_estrelas: int, db: Session       = Depends(get_db)):
    hoteis = db.query(HotelDB).filter(HotelDB.estrelas >= min_estrelas).all()
    return hoteis

@router.get("/hoteis/preco/{max_preco}", tags=["Hotéis"]) # Requisito GET por preço máximo
def listar_hoteis_por_preco(max_preco: float, db: Session = Depends     (get_db)):
    hoteis = db.query(HotelDB).filter(HotelDB.preco_diaria <= max_preco).all()
    return hoteis

@router.get("/hoteis/filtro/", tags=["Hotéis"]) # Requisito GET com múltiplos filtros
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

@router.post("/acomodacoes/criar/", tags=["Hotéis"]) # Requisito POST para acomodação
def cadastrar_acomodacao(acomodacao: AcomodacaoCreate, db: Session = Depends(get_db)):
    try:
        # Chama o service para resolver
        novo_acomodacao = acomodacao_service.criar_acomodacao(db, acomodacao)
        return novo_acomodacao
    except Exception as e:
        # Captura o erro da regra de negócio
        raise HTTPException(status_code=400, detail=str(e))
    
@router.patch("hoteis/{hotel_id}/acomodacoes/{acomodacao_id}/atualizar", tags=["Hotéis"]) # Requisito PATCH para acomodação
def atualizar_parcial_acomodacao(hotel_id: int, acomodacao_id: int, acomodacao_atualizada: AcomodacaoCreate, db: Session = Depends(get_db)):
    acomodacao = db.query(AcomodacaoDB).filter(
        AcomodacaoDB.id == acomodacao_id,
        AcomodacaoDB.hotel_id == hotel_id
    ).first()
    if acomodacao is None:
        raise HTTPException(status_code=404, detail="Acomodação não encontrada")
    
    # Atualiza apenas os campos fornecidos
    if acomodacao_atualizada.tipo is not None:
        acomodacao.tipo = acomodacao_atualizada.tipo
    if acomodacao_atualizada.capacidade is not None:
        acomodacao.capacidade = acomodacao_atualizada.capacidade
    if acomodacao_atualizada.preco_noite is not None:
        acomodacao.preco_noite = acomodacao_atualizada.preco_noite
    if acomodacao_atualizada.hotel_id is not None:
        acomodacao.hotel_id = acomodacao_atualizada.hotel_id

    db.commit()
    db.refresh(acomodacao)
    return acomodacao

@router.get("/acomodacoes/", tags=["Hotéis"]) # Requisito GET para listar acomodações
def listar_acomodacoes(db: Session = Depends(get_db)):
    return db.query(AcomodacaoDB).all() 

@router.get("/acomodacoes/{acomodacao_id}", tags=["Hotéis"]) # Requisito GET por ID de acomodação
def obter_acomodacao(acomodacao_id: int, db: Session = Depends(get_db)):
    acomodacao = db.query(AcomodacaoDB).filter(AcomodacaoDB.id == acomodacao_id).first()
    if acomodacao is None:
        raise HTTPException(status_code=404, detail="Acomodação não encontrada")
    return acomodacao

@router.get("/hoteis/{hotel_id}/acomodacoes/", tags=["Hotéis"]) # Requisito GET para listar acomodações de um hotel
def listar_acomodacoes_por_hotel(hotel_id: int, db: Session = Depends(get_db)):
    acomodacoes = db.query(AcomodacaoDB).filter(AcomodacaoDB.hotel_id == hotel_id).all()
    return acomodacoes

@router.delete("/hoteis/{hotel_id}/acomodacoes/{acomodacao_id}/delete", tags=["Hotéis"]) # Requisito DELETE para acomodação
def deletar_acomodacao(hotel_id: int, acomodacao_id: int, db: Session = Depends(get_db)):
    acomodacao = db.query(AcomodacaoDB).filter(
        AcomodacaoDB.id == acomodacao_id,
        AcomodacaoDB.hotel_id == hotel_id
    ).first()
    if acomodacao is None:
        raise HTTPException(status_code=404, detail="Acomodação não encontrada")
    db.delete(acomodacao)
    db.commit()
    return {"detail": "Acomodação deletada com sucesso"}

@router.post("/clientes/criar/", tags=["Clientes"]) # Requisito POST para cliente
def cadastrar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    try:
        # Chama o service para resolver
        novo_cliente = cliente_service.criar_cliente(db, cliente)
        return novo_cliente
    except Exception as e:
        # Captura o erro da regra de negócio
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/clientes/", tags=["Clientes"]) # Requisito GET para listar clientes
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(ClienteDB).all()

@router.get("/clientes/{cliente_id}", tags=["Clientes"]) # Requisito GET por ID de cliente
def obter_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(ClienteDB).filter(ClienteDB.id == cliente_id).first()
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@router.post("/reservas/criar/", tags=["Reservas"]) # Requisito POST para reserva
def cadastrar_reserva(reserva: ReservaCreate, db: Session = Depends(get_db)):
    try:
        # Chama o service para resolver
        nova_reserva = reserva_service.criar_reserva(db, reserva)
        return nova_reserva
    except Exception as e:
        # Captura o erro da regra de negócio
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reservas/", tags=["Reservas"]) # Requisito GET para listar reservas
def listar_reservas(db: Session = Depends(get_db)):
    return db.query(ReservaDB).all()

@router.get("/reservas/{reserva_id}", tags=["Reservas"]) # Requisito GET por ID de reserva
def obter_reserva(reserva_id: int, db: Session = Depends(get_db)):
    reserva = db.query(ReservaDB).filter(ReservaDB.id == reserva_id).first()
    if reserva is None:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return reserva

@router.get("/clientes/{cliente_id}/reservas/", tags=["Reservas"]) # Requisito GET para listar reservas de um cliente
def listar_reservas_por_cliente(cliente_id: int, db: Session = Depends(get_db)):
    reservas = db.query(ReservaDB).filter(ReservaDB.cliente_id == cliente_id).all()
    return reservas

@router.get("/acomodacoes/{acomodacao_id}/reservas/", tags=["Reservas"]) # Requisito GET para listar reservas de uma acomodação
def listar_reservas_por_acomodacao(acomodacao_id: int, db: Session = Depends(get_db)):
    reservas = db.query(ReservaDB).filter(ReservaDB.acomodacao_id == acomodacao_id).all()
    return reservas

@router.post("/clientes/{cliente_id}/reservas/{reserva_id}/pagamentos/criar/", tags=["Pagamentos"]) # Requisito POST para pagamento
def cadastrar_pagamento(cliente_id: int, reserva_id: int, pagamento: PagamentoCreate, db: Session = Depends(get_db)):
    try:
        # Verifica se a reserva pertence ao cliente
        reserva = db.query(ReservaDB).filter(
            ReservaDB.id == reserva_id,
            ReservaDB.cliente_id == cliente_id
        ).first()
        if reserva is None:
            raise HTTPException(status_code=404, detail="Reserva não encontrada para o cliente especificado")
        
        # Chama o service para resolver
        novo_pagamento = pagamento_service.criar_pagamento(db, pagamento, reserva_id)
        return novo_pagamento
    except Exception as e:
        # Captura o erro da regra de negócio
        raise HTTPException(status_code=400, detail=str(e))
    
@router.patch("/clientes/{cliente_id}/reservas/{reserva_id}/pagamentos/{pagamento_id}/atualizar", tags=["Pagamentos"]) # Requisito PATCH para pagamento
def atualizar_parcial_pagamento(cliente_id: int, reserva_id: int, pagamento_id: int, pagamento_atualizado: PagamentoCreate, db: Session = Depends(get_db)):
    pagamento = db.query(PagamentoDB).join(ReservaDB).filter(
        PagamentoDB.id == pagamento_id,
        ReservaDB.id == reserva_id,
        ReservaDB.cliente_id == cliente_id
    ).first()
    if pagamento is None:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    
    # Atualiza apenas os campos fornecidos
    if pagamento_atualizado.reserva_id is not None:
        pagamento.reserva_id = pagamento_atualizado.reserva_id
    if pagamento_atualizado.valor is not None:
        pagamento.valor = pagamento_atualizado.valor
    if pagamento_atualizado.data_pagamento is not None:
        pagamento.data_pagamento = pagamento_atualizado.data_pagamento

    db.commit()
    db.refresh(pagamento)
    return pagamento
    
    
@router.get("/pagamentos/", tags=["Pagamentos"]) # Requisito GET para listar pagamentos
def listar_pagamentos(db: Session = Depends(get_db)):
    return db.query(PagamentoDB).all()

@router.get("/clientes/{cliente_id}/reservas/{reserva_id}/pagamentos/{pagamento_id}", tags=["Pagamentos"]) # Requisito GET por ID de pagamento
def obter_pagamento(cliente_id: int, reserva_id: int, pagamento_id: int, db: Session = Depends(get_db)):
    pagamento = db.query(PagamentoDB).join(ReservaDB).filter(
        PagamentoDB.id == pagamento_id,
        ReservaDB.id == reserva_id,
        ReservaDB.cliente_id == cliente_id
    ).first()
    if pagamento is None:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return pagamento

@router.get("/clientes/{cliente_id}/reservas/{reserva_id}/pagamentos/", tags=["Pagamentos"]) # Requisito GET para listar pagamentos de uma reserva'
def listar_pagamentos_por_reserva(cliente_id: int, reserva_id: int, db: Session = Depends(get_db)):
    pagamentos = db.query(PagamentoDB).join(ReservaDB).filter(
        ReservaDB.id == reserva_id,
        ReservaDB.cliente_id == cliente_id
    ).all()
    return pagamentos

@router.get("/clientes/{cliente_id}/pagamentos/", tags=["Pagamentos"]) # Requisito GET para listar pagamentos de um cliente
def listar_pagamentos_por_cliente(cliente_id: int, db: Session = Depends(get_db)):
    pagamentos = db.query(PagamentoDB).join(ReservaDB).filter(ReservaDB.cliente_id == cliente_id).all()
    return pagamentos

@router.post("/clientes/{cliente_id}/reservas/{reserva_id}/feedback/", tags=["Feedback"]) # Requisito POST para feedback
def cadastrar_feedback(cliente_id: int, reserva_id: int, feedback: FeedbackCreate, db: Session = Depends(get_db)):
    try:
        # Verifica se a reserva pertence ao cliente
        reserva = db.query(ReservaDB).filter(
            ReservaDB.id == reserva_id,
            ReservaDB.cliente_id == cliente_id
        ).first()
        if reserva is None:
            raise HTTPException(status_code=404, detail="Reserva não encontrada para o cliente especificado")
        
        # Chama o service para resolver
        novo_feedback = FeedbackService().criar_feedback(db, feedback, reserva_id)
        return novo_feedback
    except Exception as e:
        # Captura o erro da regra de negócio
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/hoteis/{hotel_id}/feedbacks/", tags=["Feedback"]) # Requisito GET para listar feedbacks de um hotel
def listar_feedbacks_por_hotel(hotel_id: int, db: Session = Depends(get_db)):
    feedbacks = db.query(FeedbackDB).join(ReservaDB).join(AcomodacaoDB).filter(
        AcomodacaoDB.hotel_id == hotel_id
    ).all()
    return feedbacks