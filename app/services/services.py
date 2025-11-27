from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models.models import HotelDB, HotelCreate
from app.models.models import AcomodacaoDB, AcomodacaoCreate
from app.models.models import ClienteDB, ClienteCreate
from app.models.models import ReservaDB, ReservaCreate
from app.models.models import PagamentoDB, PagamentoCreate

class HotelService:
    def criar_hotel(self, db: Session, hotel: HotelCreate):
        # --- Regra de Negócio ---
        # O usuário não pode criar um hotel com 0 estrelas
        if hotel.estrelas < 1 or hotel.estrelas > 5:
            raise Exception("A classificação deve ser entre 1 e 5 estrelas")
        
        if hotel.preco_diaria < 0:
            raise Exception("O preço da diária deve ser maior que zero")
        
        if not hotel.estado or len(hotel.estado) != 2 or not hotel.estado.isalpha():
            raise Exception("O estado deve ser informado com a sigla de 2 caracteres")
        if not hotel.cidade:
            raise Exception("A cidade deve ser informada")
        if not hotel.nome:
            raise Exception("O nome do hotel deve ser informado")

        # Se passou na regra, salva no banco
        db_hotel = HotelDB(
            nome=hotel.nome,
            estrelas=hotel.estrelas,
            cidade=hotel.cidade,
            preco_diaria=hotel.preco_diaria,
            estado=hotel.estado,
            endereco=hotel.endereco,
            cep=hotel.cep,
            responsavel=hotel.responsavel,
            telefone=hotel.telefone,
        )
        db.add(db_hotel)
        db.commit()
        db.refresh(db_hotel)
        return db_hotel

    def listar_hoteis(self, db: Session):
        # Lista todos os hotéis no banco
        return db.query(HotelDB).all()

class AcomodacaoService:
    def criar_acomodacao(self, db: Session, acomodacao: AcomodacaoCreate):
        # --- Regra de Negócio ---
        if acomodacao.capacidade <= 0:
            raise Exception("A capacidade deve ser maior que zero")
        
        if acomodacao.preco_noite < 0:
            raise Exception("O preço por noite deve ser maior que zero")
        
        if not acomodacao.tipo:
            raise Exception("O tipo de acomodação deve ser informado")

        # Se passou na regra, salva no banco
        db_acomodacao = AcomodacaoDB(
            tipo=acomodacao.tipo,
            capacidade=acomodacao.capacidade,
            preco_noite=acomodacao.preco_noite,
            hotel_id=acomodacao.hotel_id,
        )
        db.add(db_acomodacao)
        db.commit()
        db.refresh(db_acomodacao)
        return db_acomodacao

    def listar_acomodacoes(self, db: Session):
        # Lista todas as acomodações no banco
        return db.query(AcomodacaoDB).all()
    
    def listar_acomodacoes_por_hotel(self, db: Session, hotel_id: int):
        # Lista todas as acomodações de um hotel específico
        return db.query(AcomodacaoDB).filter(AcomodacaoDB.hotel_id == hotel_id).all()

class ClienteService:
    def criar_cliente(self, db: Session, cliente: ClienteCreate):
        # --- Regra de Negócio ---
        if not cliente.nome:
            raise Exception("O nome do cliente deve ser informado")
        
        if not cliente.email or "@" not in cliente.email:
            raise Exception("Um email válido deve ser informado")
        
        if not cliente.cpf or len(cliente.cpf) != 11 or not cliente.cpf.isdigit():
            raise Exception("Um CPF válido de 11 dígitos deve ser informado")
        
        # Se passou na regra, salva no banco
        db_cliente = ClienteDB(
            nome=cliente.nome,
            email=cliente.email,
            telefone=cliente.telefone,
            cpf=cliente.cpf,
            birthdate=cliente.birthdate,
        )
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    def listar_clientes(self, db: Session):
        # Lista todos os clientes no banco
        return db.query(ClienteDB).all()
    def obter_cliente_por_id(self, db: Session, cliente_id: int):
        # Obtém um cliente pelo ID
        return db.query(ClienteDB).filter(ClienteDB.id == cliente_id).first()
    
class ReservaService:
    def criar_reserva(self, db: Session, reserva: ReservaCreate):
        # --- Regra de Negócio ---
        # Verifica se o cliente existe
        cliente = db.query(ClienteDB).filter(ClienteDB.id == reserva.cliente_id).first()
        if cliente is None:
            raise Exception("Cliente não encontrado")
        
        # Verifica se a acomodação existe
        acomodacao = db.query(AcomodacaoDB).filter(AcomodacaoDB.id == reserva.acomodacao_id).first()
        if acomodacao is None:
            raise Exception("Acomodação não encontrada")
        
        # Verifica se as datas são válidas
        
        if reserva.data_checkin >= reserva.data_checkout:
            raise Exception("A data de check-in deve ser anterior à data de check-out")
        
        if not reserva.data_checkin or not reserva.data_checkout:
            raise Exception("As datas de check-in e check-out devem ser informadas")
        
        # Verifica se a acomodação tem capacidade
        
        if acomodacao.capacidade <= 0:
            raise Exception("A acomodação não possui capacidade válida")
        
        # Verifica se a acomodação está disponível nas datas solicitadas
        
        reserva_existente = db.query(ReservaDB).filter(
            ReservaDB.acomodacao_id == reserva.acomodacao_id,
            and_(
                ReservaDB.data_checkin < reserva.data_checkout, # A reserva existente começou antes do novo checkout
                ReservaDB.data_checkout > reserva.data_checkin  # A reserva existente termina depois do novo checkin

        )).first()

        if reserva_existente:
            raise Exception(f"Acomodação indisponível. Já existe reserva de {reserva_existente.data_checkin} até {reserva_existente.data_checkout}")
        
        # Se passou na regra, salva no banco
        db_reserva = ReservaDB(
            cliente_id=reserva.cliente_id,
            acomodacao_id=reserva.acomodacao_id,
            last_update="",
        )
        
        db.add(db_reserva)
        db.commit()
        db.refresh(db_reserva)
        return db_reserva
    def listar_reservas(self, db: Session):
        # Lista todas as reservas no banco
        return db.query(ReservaDB).all()
    def obter_reserva_por_id(self, db: Session, reserva_id: int):
        # Obtém uma reserva pelo ID
        return db.query(ReservaDB).filter(ReservaDB.id == reserva_id).first()
    
class PagamentoService:
    def criar_pagamento(self, db: Session, pagamento: PagamentoCreate, reserva_id: int):
        # --- Regra de Negócio ---
        # Verifica se a reserva existe
        reserva = db.query(ReservaDB).filter(ReservaDB.id == reserva_id).first()
        if reserva is None:
            raise Exception("Reserva não encontrada")
        
        if pagamento.valor <= 0:
            raise Exception("O valor do pagamento deve ser maior que zero")
        
        if not pagamento.data_pagamento:
            raise Exception("A data do pagamento deve ser informada")
        
        # Se passou na regra, salva no banco
        db_pagamento = PagamentoDB(
            reserva_id=reserva_id,
            valor=pagamento.valor,
            data_pagamento=pagamento.data_pagamento,
        )
        db.add(db_pagamento)
        db.commit()
        db.refresh(db_pagamento)
        return db_pagamento
    def listar_pagamentos(self, db: Session):
        # Lista todos os pagamentos no banco
        return db.query(PagamentoDB).all()
    def obter_pagamento_por_id(self, db: Session, pagamento_id: int):
        # Obtém um pagamento pelo ID
        return db.query(PagamentoDB).filter(PagamentoDB.id == pagamento_id).first()