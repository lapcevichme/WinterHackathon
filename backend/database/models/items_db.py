from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer
from typing import Optional, TYPE_CHECKING
from database import Base

if TYPE_CHECKING:
    from .user_db import User_DB
    
class Items_DB(Base):
    __tablename__ = "items"
    
    item_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    casino_id: Mapped[int] = mapped_column(ForeignKey("casino.item_id"), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    user: Mapped[Optional['User_DB']] = relationship('User_DB', back_populates='items')