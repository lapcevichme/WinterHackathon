from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.sql import func
from typing import TYPE_CHECKING
from database import Base

if TYPE_CHECKING:
    from .user_db import User_DB

class RefreshToken_DB(Base):
    __tablename__ = "refresh_tokens"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), nullable=False)
    expires_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    is_blacklisted: Mapped[bool] = mapped_column(Boolean, default=False)
    
    user: Mapped['User_DB'] = relationship('User_DB', back_populates='refresh_tokens')