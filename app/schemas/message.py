from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional
from datetime import datetime

class MessageBase(BaseModel):
    message_id: str = Field(..., min_length=1, max_length=100)
    session_id: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    timestamp: datetime
    sender: Literal["user", "system"]

class MessageCreate(MessageBase):
    pass

class MessageMetadata(BaseModel):
    word_count: int
    character_count: int
    processed_at: datetime

class MessageOut(MessageBase):
    metadata: MessageMetadata

class MessagesPage(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[MessageOut]
