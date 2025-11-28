import random
from database import BaseDao
from database.models import Casino_DB

item = BaseDao(Casino_DB)

async def get_random_item():
    rare = ["gold", "often", "seldom", "never", "legenda"]
    s = random.randint(1, 100)
    itog_rare = ""
    if s > 90:
        itog_rare = "legenda"
    elif s > 75:
        itog_rare = "never"
    elif s > 55:
        itog_rare = "seldom"
    elif s > 30:
        itog_rare = "often"
    else:
        itog_rare = "gold"
    
    items = await item.get_all_name_by_rare(itog_rare)
    return items[random.randint(1, len(items))]