from pydantic import BaseModel, ConfigDict, Field, EmailStr
from uuid import UUID

from domain.common import TimestampModel

class UserModel(TimestampModel):
    """User account representation."""
    # Configure ORM conversion and drop fields set to their defaults during serialization.
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID = Field(...)
    email: EmailStr = Field(..., description="User e-mail")
    
    username: str | None = Field(None, description="User's username")
    display_name: str | None = Field(None, description="Public display name")
    profile_pic_url: str | None = Field(None)
    max_score: int = Field(0)
    score: int = Field(0)
    level: int = Field(0)
    amount: int = Field(0)
    energy: int = Field(0)
    role: str = Field("player")
    banned: bool
    
    # TODO: Make this field returned only when ?expand=roles
    # Roles list is intentionally optional so it is omitted unless expansion is requested.
    roles: list[str] = Field(
        alias="role_slugs",
        default_factory=list,
        description="User's roles."
    )


class UserPatch(BaseModel):
    username: str | None = Field(None, description="User's username")
    display_name: str | None = Field(None, description="Public display name")
    profile_pic_url: str | None = Field(None)


class UserRolesUpdate(BaseModel):
    roles: list[str] = Field(default_factory=list, description="Role slugs to assign")


class TeamModel(BaseModel):
    id: UUID
    name: str
    score: int
    max_score: int


class TeamJoinRequest(BaseModel):
    team_id: UUID
