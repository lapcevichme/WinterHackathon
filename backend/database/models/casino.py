from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database import Base
    
class Casino_DB(Base):
    __tablename__ = "casino"
    
    item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, default=0)
    amoji: Mapped[str] = mapped_column(String(20), default=0)
    color: Mapped[str] = mapped_column(String(20), default=0)
    
    rare: Mapped[str] = mapped_column(String(100), nullable=False)