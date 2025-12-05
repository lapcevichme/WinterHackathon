from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, EmailStr, HttpUrl, constr
from datetime import date
from uuid import UUID

from domain.common import TimestampModel

class UserModel(TimestampModel):
    """User account representation."""
    # Configure ORM conversion and drop fields set to their defaults during serialization.
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID = Field(...)
    email: EmailStr = Field(..., description="User e-mail")
    
    username: str | None = Field(None, description="User's display name")
    profile_pic_url: HttpUrl | None = Field(None)
    bio: str | None = Field(None)
    language_code: Annotated[str, constr(min_length=2, max_length=2)] | None = Field(None)
    
    is_onboarded: bool
    banned: bool
    
    # TODO: Make this field returned only when ?expand=roles
    # Roles list is intentionally optional so it is omitted unless expansion is requested.
    roles: list[str] = Field(
        alias="role_slugs",
        default_factory=list,
        description="User's roles."
    )


class UserPatch(BaseModel):
    username: str | None = Field(None, description="User's display name")
    profile_pic_url: str | None = Field(None)
    bio: str | None = Field(None)
    birth_date: date | None = Field(None)
    language_code: Annotated[str, constr(min_length=2, max_length=2)] | None = Field(None)


class UserRolesUpdate(BaseModel):
    roles: list[str] = Field(default_factory=list, description="Role slugs to assign")
