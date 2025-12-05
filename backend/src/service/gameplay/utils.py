import random
import string
from datetime import datetime, UTC


def generate_qr_token(length: int = 10) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choices(alphabet, k=length))


def now_utc() -> datetime:
    return datetime.now(UTC)


def refill_energy(
    current_energy: int,
    updated_at: datetime | None,
    max_energy: int = 10,
    seconds_per_point: int = 300,
) -> tuple[int, int]:
    """
    Refill energy based on time passed since updated_at.
    Returns tuple of (new_energy, seconds_until_next_refill).
    """
    if updated_at is None:
        return current_energy, 0

    now = now_utc()
    elapsed = int((now - updated_at).total_seconds())
    gained = elapsed // seconds_per_point
    new_energy = min(max_energy, current_energy + gained)
    if new_energy >= max_energy:
        return max_energy, 0
    seconds_until_next = seconds_per_point - (elapsed % seconds_per_point)
    return new_energy, seconds_until_next
