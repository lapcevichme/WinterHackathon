from typing import Annotated
from pydantic import BaseModel, Field, HttpUrl, constr
from uuid import UUID


class UserShare(BaseModel):
    """
    User schema making possible to share other users public profile data.
    """
    id: UUID = Field(...)
    
    username: str | None = Field(None, description="User's display name")
    profile_pic_url: HttpUrl | None = Field(None)
    bio: str | None = Field(None)
    language_code: Annotated[str, constr(min_length=2, max_length=2)] | None = Field(None)

class UserBrief(BaseModel):
    id: UUID = Field(...)
    username: str | None = Field(None, description="User's display name")
    profile_pic_url: HttpUrl | None = Field(None)
