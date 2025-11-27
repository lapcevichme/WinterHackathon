from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from database import Base
    
class Casino_DB(Base):
    __tablename__ = "casino"
    
    item_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, default=0)
    amoji: Mapped[str] = mapped_column(String(20), default=0)
    color: Mapped[str] = mapped_column(String(20), default=0)
    
    