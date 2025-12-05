from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Uuid, String, Boolean, DateTime, Text, Index, Integer

from ..table_base import Base
from ..mixins import TimestampMixin

class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), default=uuid4, primary_key=True)
    
    # Credentials
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Profile info
    username: Mapped[str | None] = mapped_column(String(50), nullable=True, unique=True)
    display_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    profile_pic_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    # Game progression (from legacy schema)
    max_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    energy: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="player")
    
    # Service
    banned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    auth_version: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1, server_default="1"
    )

    __table_args__ = (
        # GIN trigram indexes for fast text search
        Index(
            'users_username_trgm',
            'username',
            postgresql_using='gin',
            postgresql_ops={'username': 'gin_trgm_ops'}
        ),
        Index(
            'users_email_trgm',
            'email',
            postgresql_using='gin',
            postgresql_ops={'email': 'gin_trgm_ops'}
        ),
    )
    
    roles: Mapped[list["Role"]] = relationship(  # pyright: ignore
        "Role",
        secondary="user_roles",
        back_populates="users",
        lazy="selectin",
    )
    
    @property
    def role_slugs(self) -> list[str]:
        return [role.slug for role in self.roles]

    def has_roles(self, *slugs: str) -> bool:
        if not slugs:
            return True
        owned = set(self.role_slugs)
        return all(slug in owned for slug in slugs)

    def bump_auth_version(self) -> None:
        self.auth_version = (self.auth_version or 0) + 1
