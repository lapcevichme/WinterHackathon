from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional, TYPE_CHECKING
import uuid
from database import Base

if TYPE_CHECKING:
    from .user_db import User_DB
    
class Token_qr_DB(Base):
    __tablename__ = "token_qr"
    
    
    token_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    times: Mapped[int] = mapped_column(Integer, default=300)
    token: Mapped[String] = mapped_column(String(100))
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey('users.user_id'), 
        nullable=False
    )
    item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey('items.item_id'), 
        nullable=False
    )
