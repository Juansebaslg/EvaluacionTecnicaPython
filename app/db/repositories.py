from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.models import Message


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    # Crear un mensaje
    def create(self, model: Message):
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    # Buscar por message_id
    def get_by_message_id(self, message_id: str):
        return self.db.query(Message).filter(Message.message_id == message_id).first()

    # Listar mensajes de una sesión
    def list_by_session(self, session_id: str, sender: str = None, limit: int = 10, offset: int = 0):
        query = self.db.query(Message).filter(Message.session_id == session_id)
        if sender:
            query = query.filter(Message.sender == sender)
        return query.offset(offset).limit(limit).all()

    # Contar mensajes de una sesión
    def count_by_session(self, session_id: str, sender: str = None):
        query = self.db.query(Message).filter(Message.session_id == session_id)
        if sender:
            query = query.filter(Message.sender == sender)
        return query.count()

    #  Buscar mensajes por texto dentro de una sesión
    def search_messages(self, session_id: str, query_text: str, limit: int = 10, offset: int = 0):
        query = (
            self.db.query(Message)
            .filter(Message.session_id == session_id)
            .filter(Message.content.ilike(f"%{query_text}%"))
            .offset(offset)
            .limit(limit)
        )
        return query.all()

    # Contar resultados de búsqueda
    def count_search_messages(self, session_id: str, query_text: str):
        return (
            self.db.query(Message)
            .filter(Message.session_id == session_id)
            .filter(Message.content.ilike(f"%{query_text}%"))
            .count()
        )

