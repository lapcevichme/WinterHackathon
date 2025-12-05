from enum import Enum


class PrizeType(str, Enum):
    ITEM = "ITEM"
    MONEY = "MONEY"
    TRASH = "TRASH"


class ItemStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    REDEEMED = "REDEEMED"


class LeaderboardType(str, Enum):
    PLAYERS = "PLAYERS"
    DEPARTMENTS = "DEPARTMENTS"


class Trend(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    SAME = "SAME"
