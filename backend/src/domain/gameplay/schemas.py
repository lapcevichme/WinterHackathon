from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from .enums import PrizeType, ItemStatus, LeaderboardType, Trend


class Balance(BaseModel):
    amount: int
    currency_symbol: str = Field("❄️")


class Prize(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    type: PrizeType
    amount: int
    emoji: str
    color_hex: str


class InventoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    prize_id: UUID
    name: str
    type: PrizeType
    status: ItemStatus
    amount: int
    emoji: str
    color_hex: str


class ProfileResponse(BaseModel):
    id: UUID
    username: str | None
    display_name: str | None
    department: str | None
    avatar_url: str | None
    level: int
    xp: int
    max_xp: int
    inventory: list[InventoryItem] = Field(default_factory=list)


class ProfilePatch(BaseModel):
    display_name: str | None = None
    avatar_url: str | None = None


class RedeemTokenResponse(BaseModel):
    redeem_token: str
    expires_in_seconds: int = 300


class EnergyState(BaseModel):
    current: int
    max: int
    next_refill_in_seconds: int


class UserSummary(BaseModel):
    id: UUID
    display_name: str | None
    balance: Balance
    energy: EnergyState




class BetRequest(BaseModel):
    bet: int = Field(..., gt=0)


class SpinResponse(BaseModel):
    winner: Prize
    new_balance: Balance


class LeaderboardEntry(BaseModel):
    rank: int
    name: str
    score: int
    trend: Trend = Trend.SAME


class GameStartResponse(BaseModel):
    session_id: UUID
    energy_left: int


class GameInfo(BaseModel):
    slug: str
    name: str
    energy_cost: int
    

class MainResponse(BaseModel):
    user_summary: UserSummary
    games: list[GameInfo] = Field(default_factory=list)
    # quests: list[QuestInfo] = Field(default_factory=list)


class GameScoreRequest(BaseModel):
    session_id: UUID
    score: int = Field(..., ge=0)


class GameScoreResponse(BaseModel):
    success: bool = True
    team_score_added: int
    total_team_score: int | None = None


class AdminRedeemRequest(BaseModel):
    redeem_token: str


class AdminRedeemResponse(BaseModel):
    success: bool = True
    item_name: str
    user_display_name: str | None
    redeemed_at: datetime
