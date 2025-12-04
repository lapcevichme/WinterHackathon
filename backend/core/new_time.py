from datetime import datetime, timezone
from database.models import User_DB
from database import BaseDao
user_basedao = BaseDao(User_DB)
async def get_time_diff_seconds(user: User_DB) -> float:
    current_time = datetime.now(timezone.utc)
    time_diff = current_time - user.update_at
    return time_diff.total_seconds()


async def research_user_energy(user: User_DB):
    seconds = get_time_diff_seconds(user)
    if user.energy + seconds // 300 >= 10:
        user.energy = 10
    else:
        user.energy = user.energy + seconds // 300
    if user.energy != 10:
        next_refill = seconds % 300
    else:
        next_refill = 0
    user_basedao.update_entity(user.user_id, user)
    return next_refill