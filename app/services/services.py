from sqlalchemy.orm import Session
from app.models.models import HotelDB, HotelCreate, AcomodacaoDB, AcomodacaoCreate

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