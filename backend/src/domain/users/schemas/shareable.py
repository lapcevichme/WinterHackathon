from pydantic import BaseModel, Field
from uuid import UUID


class UserShare(BaseModel):
    """
    User schema making possible to share other users public profile data.
    """
    id: UUID = Field(...)
    
    username: str | None = Field(None, description="User's username")
    display_name: str | None = Field(None, description="Public display name")
    profile_pic_url: str | None = Field(None)

class UserBrief(BaseModel):
    id: UUID = Field(...)
    username: str | None = Field(None, description="User's username")
    display_name: str | None = Field(None, description="Public display name")
    profile_pic_url: str | None = Field(None)
