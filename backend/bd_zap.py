# populate_database.py
import asyncio
import random
from datetime import datetime
from database import BaseDao
from database.models import User_DB, Team_DB, Casino_DB, Items_DB, RefreshToken_DB
from core.security import get_password_hash

class DatabasePopulator:
    def __init__(self):
        self.user_dao = BaseDao(User_DB)
        self.team_dao = BaseDao(Team_DB)
        self.casino_dao = BaseDao(Casino_DB)
        self.items_dao = BaseDao(Items_DB)
        self.refresh_token_dao = BaseDao(RefreshToken_DB)
    
    async def clear_database(self):
        """Очистка базы данных (опционально)"""
        print("🧹 Очистка базы данных...")
        try:
            # Удаляем данные в правильном порядке (из-за foreign keys)
            items = await self.items_dao.get_entities()
            for item in items:
                await self.items_dao.delete_entity(item.item_id)
            
            tokens = await self.refresh_token_dao.get_entities()
            for token in tokens:
                await self.refresh_token_dao.delete_entity(token.id)
            
            users = await self.user_dao.get_entities()
            for user in users:
                await self.user_dao.delete_entity(user.user_id)
            
            casino_items = await self.casino_dao.get_entities()
            for item in casino_items:
                await self.casino_dao.delete_entity(item.item_id)
            
            teams = await self.team_dao.get_entities()
            for team in teams:
                await self.team_dao.delete_entity(team.team_id)
                
            print("✅ База данных очищена")
        except Exception as e:
            print(f"⚠️ Ошибка при очистке: {e}")

    async def create_teams(self):
        """Создание тестовых команд"""
        print("\n🏆 СОЗДАНИЕ КОМАНД")
        
        teams_data = [
            {"team_name": "Dragons", "max_score": 1500, "money": 5000},
            {"team_name": "Wizards", "max_score": 1200, "money": 3000},
            {"team_name": "Warriors", "max_score": 1800, "money": 7000},
            {"team_name": "Rogues", "max_score": 900, "money": 2000},
        ]
        
        created_teams = []
        for team_data in teams_data:
            team = await self.team_dao.create_entity(team_data)
            created_teams.append(team)
            print(f"✅ Создана команда: {team.team_name}")
        
        return created_teams

    async def create_users(self, teams):
        """Создание тестовых пользователей"""
        print("\n👥 СОЗДАНИЕ ПОЛЬЗОВАТЕЛЕЙ")
        
        users_data = [
            # Администраторы
            {
                "username": "admin",
                "password": get_password_hash("admin123"),
                "email": "admin@casino.com",
                "max_score": 0,
                "money": 10000,
                "role": "admin",
                "url": "https://example.com/admin"
            },
            {
                "username": "superadmin",
                "password": get_password_hash("super123"),
                "email": "superadmin@casino.com", 
                "max_score": 0,
                "money": 15000,
                "role": "admin",
                "url": None
            },
            
            # Модераторы
            {
                "username": "moderator1",
                "password": get_password_hash("mod123"),
                "email": "mod1@casino.com",
                "max_score": 500,
                "money": 5000,
                "role": "moderator",
                "team_id": teams[0].team_id if teams else None
            },
            {
                "username": "moderator2", 
                "password": get_password_hash("mod123"),
                "email": "mod2@casino.com",
                "max_score": 300,
                "money": 4000,
                "role": "moderator",
                "team_id": teams[1].team_id if teams else None
            },
            
            # Обычные игроки
            {
                "username": "player1",
                "password": get_password_hash("player123"),
                "email": "player1@casino.com",
                "max_score": 250,
                "money": 1000,
                "role": "player",
                "team_id": teams[0].team_id if teams else None
            },
            {
                "username": "player2",
                "password": get_password_hash("player123"),
                "email": "player2@casino.com",
                "max_score": 180,
                "money": 800,
                "role": "player", 
                "team_id": teams[0].team_id if teams else None
            },
            {
                "username": "player3",
                "password": get_password_hash("player123"),
                "email": "player3@casino.com",
                "max_score": 420,
                "money": 1500,
                "role": "player",
                "team_id": teams[1].team_id if teams else None
            },
            {
                "username": "rich_player",
                "password": get_password_hash("rich123"),
                "email": "rich@casino.com", 
                "max_score": 50,
                "money": 10000,
                "role": "player",
                "team_id": teams[2].team_id if teams else None
            },
            {
                "username": "newbie",
                "password": get_password_hash("new123"),
                "email": "newbie@casino.com",
                "max_score": 10,
                "money": 100,
                "role": "player",
                "team_id": None  # Без команды
            }
        ]
        
        created_users = []
        for user_data in users_data:
            user = await self.user_dao.create_entity(user_data)
            created_users.append(user)
            role_icon = "👑" if user.role == "admin" else "🛡️" if user.role == "moderator" else "🎮"
            print(f"✅ {role_icon} Создан пользователь: {user.username} ({user.role}) - {user.money} монет")
        
        return created_users

    async def create_casino_prizes(self):
        """Создание призов для казино"""
        print("\n🎰 СОЗДАНИЕ ПРИЗОВ КАЗИНО")
        
        prizes_data = [
            # COMMON (55% шанс)
            {
                "name": "Монеты удачи",
                "type": "currency",
                "description": "Небольшая сумма монет для продолжения игры",
                "amount": 50,
                "amoji": "🪙",
                "color": "#9E9E9E",
                "rare": "COMMON"
            },
            {
                "name": "Простое зелье",
                "type": "potion", 
                "description": "Восстанавливает немного здоровья",
                "amount": 25,
                "amoji": "🧪",
                "color": "#9E9E9E", 
                "rare": "COMMON"
            },
            {
                "name": "Деревянный меч",
                "type": "weapon",
                "description": "Простое оружие для начинающих",
                "amount": 30,
                "amoji": "⚔️",
                "color": "#9E9E9E",
                "rare": "COMMON"
            },
            {
                "name": "Кожаный доспех",
                "type": "armor",
                "description": "Базовая защита от врагов",
                "amount": 20,
                "amoji": "🛡️",
                "color": "#9E9E9E",
                "rare": "COMMON"
            },
            
            # RARE (20% шанс)
            {
                "name": "Золотые монеты",
                "type": "currency", 
                "description": "Значительная сумма для улучшения снаряжения",
                "amount": 15,
                "amoji": "💰",
                "color": "#2196F3",
                "rare": "RARE"
            },
            {
                "name": "Сильное зелье",
                "type": "potion",
                "description": "Восстанавливает большое количество здоровья",
                "amount": 10,
                "amoji": "🔮",
                "color": "#2196F3",
                "rare": "RARE"
            },
            {
                "name": "Стальной меч",
                "type": "weapon",
                "description": "Острое оружие с хорошим уроном",
                "amount": 12,
                "amoji": "🗡️",
                "color": "#2196F3",
                "rare": "RARE"
            },
            
            # EPIC (15% шанс) 
            {
                "name": "Мешок сокровищ",
                "type": "currency",
                "description": "Огромное богатство для настоящих победителей",
                "amount": 8,
                "amoji": "💎",
                "color": "#E91E63", 
                "rare": "EPIC"
            },
            {
                "name": "Эликсир бессмертия",
                "type": "potion",
                "description": "Дарует временную неуязвимость в бою",
                "amount": 5,
                "amoji": "⚗️",
                "color": "#E91E63",
                "rare": "EPIC"
            },
            {
                "name": "Магический посох",
                "type": "weapon", 
                "description": "Излучает мощную магическую энергию",
                "amount": 6,
                "amoji": "🔱",
                "color": "#E91E63",
                "rare": "EPIC"
            },
            
            # LEGENDARY (10% шанс)
            {
                "name": "Сундук дракона",
                "type": "currency",
                "description": "Легендарное сокровище из драконьей пещеры",
                "amount": 3,
                "amoji": "🐉",
                "color": "#FFD700",
                "rare": "LEGENDARY"
            },
            {
                "name": "Фениксово перо",
                "type": "artifact",
                "description": "Мифический артефакт с силой возрождения",
                "amount": 2,
                "amoji": "🔥",
                "color": "#FFD700", 
                "rare": "LEGENDARY"
            },
            {
                "name": "Экскалибур",
                "type": "weapon",
                "description": "Легендарный меч короля Артура",
                "amount": 1,
                "amoji": "⚜️",
                "color": "#FFD700",
                "rare": "LEGENDARY"
            }
        ]
        
        created_prizes = []
        for prize_data in prizes_data:
            prize = await self.casino_dao.create_entity(prize_data)
            created_prizes.append(prize)
            
            rare_icons = {
                "COMMON": "⚪",
                "RARE": "🔵", 
                "EPIC": "🟣",
                "LEGENDARY": "🟡"
            }
            rare_icon = rare_icons.get(prize.rare, "⚫")
            print(f"✅ {rare_icon} Создан приз: {prize.name} ({prize.rare}) - {prize.amount} шт.")
        
        return created_prizes

    async def create_user_items(self, users, prizes):
        """Создание тестовых предметов у пользователей"""
        print("\n🎁 СОЗДАНИЕ ПРЕДМЕТОВ ПОЛЬЗОВАТЕЛЕЙ")
        
        # Выбираем обычных игроков (не админов/модераторов)
        players = [user for user in users if user.role == "player"]
        
        if not players or not prizes:
            print("⚠️ Нет игроков или призов для создания предметов")
            return
        
        items_created = 0
        for player in players[:5]:  # Первым 5 игрокам даем предметы
            # Случайное количество предметов (1-3)
            num_items = random.randint(1, 3)
            for _ in range(num_items):
                # Выбираем случайный приз
                prize = random.choice(prizes)
                
                item_data = {
                    "user_id": player.user_id,
                    "casino_id": prize.item_id
                }
                
                await self.items_dao.create_entity(item_data)
                items_created += 1
        
        print(f"✅ Создано {items_created} предметов у игроков")

    async def generate_test_data(self):
        """Генерация дополнительных тестовых данных"""
        print("\n🧪 СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ")
        
        # Создаем дополнительных тестовых пользователей
        test_users = []
        for i in range(5):
            user_data = {
                "username": f"test_user_{i+1}",
                "password": get_password_hash("test123"),
                "email": f"test{i+1}@casino.com",
                "max_score": random.randint(0, 500),
                "money": random.randint(100, 2000),
                "role": "player",
                "team_id": None
            }
            user = await self.user_dao.create_entity(user_data)
            test_users.append(user)
        
        print(f"✅ Создано {len(test_users)} тестовых пользователей")

    async def show_statistics(self):
        """Показать статистику базы данных"""
        print("\n📊 СТАТИСТИКА БАЗЫ ДАННЫХ")
        
        users = await self.user_dao.get_entities()
        teams = await self.team_dao.get_entities()
        prizes = await self.casino_dao.get_entities()
        items = await self.items_dao.get_entities()
        
        users_list = list(users) if users else []
        teams_list = list(teams) if teams else []
        prizes_list = list(prizes) if prizes else []
        items_list = list(items) if items else []
        
        print(f"👥 Пользователи: {len(users_list)}")
        print(f"🏆 Команды: {len(teams_list)}")
        print(f"🎰 Призы казино: {len(prizes_list)}")
        print(f"🎁 Предметы игроков: {len(items_list)}")
        
        # Статистика по ролям
        role_stats = {}
        for user in users_list:
            role_stats[user.role] = role_stats.get(user.role, 0) + 1
        
        print("👑 Распределение по ролям:")
        for role, count in role_stats.items():
            print(f"   {role}: {count}")

    async def populate(self, clear_existing=False):
        """Основной метод заполнения базы данных"""
        print("🚀 ЗАПУСК ЗАПОЛНЕНИЯ БАЗЫ ДАННЫХ")
        print("=" * 50)
        
        try:
            if clear_existing:
                await self.clear_database()
            
            # Создаем команды
            teams = await self.create_teams()
            
            # Создаем пользователей
            users = await self.create_users(teams)
            
            # Создаем призы казино
            prizes = await self.create_casino_prizes()
            
            # Создаем предметы пользователей
            await self.create_user_items(users, prizes)
            
            # Генерируем тестовые данные
            await self.generate_test_data()
            
            # Показываем статистику
            await self.show_statistics()
            
            print("\n" + "=" * 50)
            print("🎉 БАЗА ДАННЫХ УСПЕШНО ЗАПОЛНЕНА!")
            print("=" * 50)
            
            # Показываем тестовые учетные данные
            print("\n🔐 ТЕСТОВЫЕ УЧЕТНЫЕ ЗАПИСИ:")
            print("   👑 Администратор: admin / admin123")
            print("   🛡️ Модератор: moderator1 / mod123") 
            print("   🎮 Игрок: player1 / player123")
            print("   💰 Богатый игрок: rich_player / rich123")
            print("   🆕 Новичок: newbie / new123")
            
        except Exception as e:
            print(f"❌ Ошибка при заполнении базы данных: {e}")
            raise

async def main():
    """Основная функция"""
    populator = DatabasePopulator()
    
    # Заполняем базу данных (clear_existing=True для очистки существующих данных)
    await populator.populate(clear_existing=True)

if __name__ == "__main__":
    asyncio.run(main())