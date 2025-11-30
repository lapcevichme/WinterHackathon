from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from typing import TYPE_CHECKING
import uuid
from database import Base

if TYPE_CHECKING:
    from .user_db import User_DB

class RefreshToken_DB(Base):
    __tablename__ = "refresh_tokens"
    
    token_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey('users.user_id'), 
        nullable=False
    )
    
    expires_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    
    user: Mapped['User_DB'] = relationship('User_DB', back_populates='refresh_tokens', lazy="joined")