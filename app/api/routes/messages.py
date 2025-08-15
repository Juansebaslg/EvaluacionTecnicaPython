from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.api.deps import get_db
from app.core.config import settings
from app.core.errors import AppException
from app.db.models import Message as MessageModel
from app.db.repositories import MessageRepository
from app.schemas.message import MessageCreate, MessageOut, MessageMetadata, MessagesPage
from app.services.processing import mask_banned_words, compute_metadata

router = APIRouter(prefix="/api/messages", tags=["messages"])

@router.post("", response_model=dict)
def create_message(payload: MessageCreate, db: Session = Depends(get_db)):
    repo = MessageRepository(db)

    # Check uniqueness of message_id
    if repo.get_by_message_id(payload.message_id):
        raise AppException(
            code="DUPLICATE_MESSAGE_ID",
            message="Formato de mensaje inválido",
            details="message_id ya existe",
            http_status=409,
        )

    # Filter content and compute metadata
    filtered_content, had_profanity = mask_banned_words(payload.content, settings.BANNED_WORDS)
    word_count, char_count, processed_at = compute_metadata(filtered_content)

    model = MessageModel(
        message_id=payload.message_id,
        session_id=payload.session_id,
        content=filtered_content,
        timestamp=payload.timestamp,
        sender=payload.sender,
        word_count=word_count,
        character_count=char_count,
        contains_profanity=had_profanity,
        processed_at=processed_at,
    )
    model = repo.create(model)

    response: MessageOut = MessageOut(
        **payload.model_dump(),
        content=model.content,
        metadata=MessageMetadata(
            word_count=model.word_count,
            character_count=model.character_count,
            processed_at=model.processed_at,
        ),
    )

    return {"status": "success", "data": response.model_dump()}

@router.get("/{session_id}", response_model=dict)
def list_messages(
    session_id: str,
    sender: Optional[str] = Query(None, description="Filtra por remitente: user o system"),
    limit: int = Query(settings.DEFAULT_LIMIT, ge=1, le=settings.MAX_LIMIT),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    if sender not in (None, "user", "system"):
        raise AppException(
            code="INVALID_FORMAT",
            message="Formato de mensaje inválido",
            details="El campo 'sender' debe ser 'user' o 'system' si se especifica",
            http_status=422,
        )

    repo = MessageRepository(db)
    items = repo.list_by_session(session_id=session_id, sender=sender, limit=limit, offset=offset)
    total = repo.count_by_session(session_id=session_id, sender=sender)

    def to_out(m: MessageModel) -> MessageOut:
        return MessageOut(
            message_id=m.message_id,
            session_id=m.session_id,
            content=m.content,
            timestamp=m.timestamp,
            sender=m.sender,
            metadata=MessageMetadata(
                word_count=m.word_count,
                character_count=m.character_count,
                processed_at=m.processed_at,
            ),
        )

    page = MessagesPage(
        total=total,
        limit=limit,
        offset=offset,
        items=[to_out(m).model_dump() for m in items],  # convert to dicts
    )

    return {"status": "success", "data": page.model_dump()}
