from datetime import datetime, UTC
from uuid import UUID, uuid4
from typing import TYPE_CHECKING
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .table_base import Base
from .mixins import TimestampMixin

if TYPE_CHECKING:
    from .users.users_table import User


class Team(TimestampMixin, Base):
    __tablename__ = "teams"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    max_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    users: Mapped[list["User"]] = relationship(
        "User", back_populates="team", lazy="selectin"
    )


class Prize(TimestampMixin, Base):
    __tablename__ = "prizes"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)  # Enum by validator
    amount: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    emoji: Mapped[str] = mapped_column(String(20), default="", nullable=False)
    color_hex: Mapped[str] = mapped_column(String(20), default="#FFFFFF", nullable=False)

    items: Mapped[list["InventoryItem"]] = relationship(
        "InventoryItem",
        back_populates="prize",
        lazy="selectin",
        cascade="all, delete-orphan",
    )


class InventoryItem(TimestampMixin, Base):
    __tablename__ = "inventory_items"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    prize_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("prizes.id"), nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="AVAILABLE")

    prize: Mapped["Prize"] = relationship("Prize", back_populates="items", lazy="joined")
    user: Mapped["User"] = relationship("User", back_populates="items", lazy="joined")


class TokenQR(TimestampMixin, Base):
    __tablename__ = "token_qr"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    token: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    item_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("inventory_items.id"),
        nullable=False,
    )


class GameSession(TimestampMixin, Base):
    __tablename__ = "game_sessions"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    game_id: Mapped[str] = mapped_column(String(100), nullable=False)
    energy_cost: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class LaunchCode(TimestampMixin, Base):
    __tablename__ = "launch_codes"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    user_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    session_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("game_sessions.id"), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
