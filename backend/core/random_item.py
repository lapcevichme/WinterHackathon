import random
from database import BaseDao
from database.models import Casino_DB

item = BaseDao(Casino_DB)

async def get_random_item():
    rare = {"COMMON":"#FF9E9E9E", "RARE":"#FF2196F3", "EPIC":"#FFE91E63", "LEGENDARY":"#FFFFD700"}
    rare_price = {"COMMON":0, "RARE":10, "EPIC":40, "LEGENDARY":100}
    s = random.randint(1, 100)
    itog_rare = ""
    if s > 90:
        itog_rare = "LEGENDARY"
    elif s > 75:
        itog_rare = "EPIC"
    elif s > 55:
        itog_rare = "RARE"
    elif s > 30:
        itog_rare = "COMMON"
    
    items = await item.get_all_name_by_rare(itog_rare)
    return {"item": items[random.randint(1, len(items))], "itog_rare":rare[itog_rare], "itog_rare_price":rare_price[itog_rare]}