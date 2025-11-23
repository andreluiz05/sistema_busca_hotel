from sqlalchemy.orm import Session
from app.models.models import HotelDB, HotelCreate

class HotelService:
    def criar_hotel(self, db: Session, hotel: HotelCreate):
        # --- Regra de Negócio ---
        # O usuário não pode criar um hotel com 0 estrelas
        if hotel.estrelas < 1 or hotel.estrelas > 5:
            raise Exception("A classificação deve ser entre 1 e 5 estrelas")

        # Se passou na regra, salva no banco
        db_hotel = HotelDB(
            nome=hotel.nome,
            estrelas=hotel.estrelas,
            # ... complete com os campos
        )
        db.add(db_hotel)
        db.commit()
        db.refresh(db_hotel)
        return db_hotel

    def listar_hoteis(self, db: Session):
        # Lista todos os hotéis no banco
        return db.query(HotelDB).all()