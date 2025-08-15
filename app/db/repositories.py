from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models import Message

class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_message_id(self, message_id: str) -> Optional[Message]:
        return self.db.get(Message, message_id)

    def create(self, message: Message) -> Message:
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def list_by_session(
        self, session_id: str, sender: Optional[str], limit: int, offset: int
    ) -> List[Message]:
        stmt = select(Message).where(Message.session_id == session_id)
        if sender:
            stmt = stmt.where(Message.sender == sender)
        stmt = stmt.order_by(Message.timestamp.asc()).limit(limit).offset(offset)
        return list(self.db.execute(stmt).scalars())

    def count_by_session(self, session_id: str, sender: Optional[str]) -> int:
        from sqlalchemy import func
        stmt = select(func.count()).select_from(Message).where(Message.session_id == session_id)
        if sender:
            stmt = stmt.where(Message.sender == sender)
        return self.db.execute(stmt).scalar_one()
