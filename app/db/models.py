from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Boolean, Index
from datetime import datetime
from app.db.base import Base

class Message(Base):
    __tablename__ = "messages"

    message_id: Mapped[str] = mapped_column(String(100), primary_key=True, index=True)
    session_id: Mapped[str] = mapped_column(String(100), index=True)
    content: Mapped[str] = mapped_column(String)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    sender: Mapped[str] = mapped_column(String(10), index=True)  # "user" or "system"

    word_count: Mapped[int] = mapped_column(Integer)
    character_count: Mapped[int] = mapped_column(Integer)
    contains_profanity: Mapped[bool] = mapped_column(Boolean, default=False)
    processed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        Index("idx_session_id_timestamp", "session_id", "timestamp"),
    )
