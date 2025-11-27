import aiohttp
import asyncio
import json

async def test_auth_api():
    base_url = 'http://127.0.0.1:8000/v1/auth'
    
    async with aiohttp.ClientSession() as session:
        print("=== РЕГИСТРАЦИЯ ===")
        register_data = {
            'username': 'Alice', 
            'password': '38752598y963896', 
            'email': 'govno@mail.ru'
        }
        async with session.post(f'{base_url}/register', json=register_data) as response:
            print(f"Статус: {response.status}")
            response_text = await response.text()
            print(f"Тело ответа: {response_text}")
        
        print("\n=== ЛОГИН ===")
        login_data = {
            'username': 'Alice', 
            'password': '38752598y963896'
        }
        async with session.post(f'{base_url}/login', json=login_data) as response:
            print(f"Статус: {response.status}")
            response_text = await response.text()
            print(f"Тело ответа: {response_text}")
            
            if response.status == 200:
                try:
                    response_data = json.loads(response_text)
                    token = response_data.get('access_token')
                    print(f"✅ Токен получен успешно!")
                    return token
                except Exception as e:
                    print(f"❌ Ошибка парсинга токена: {e}")
                    return None
            else:
                print("❌ Логин не удался")
                return None

async def test_with_token(token):
    base_url = 'http://127.0.0.1:8000/v1/auth'
    
    async with aiohttp.ClientSession() as session:
        headers = {'Authorization': f'Bearer {token}'}
        
        print("\n=== ПРОВЕРКА ТОКЕНА ===")
        async with session.get(f'{base_url}/verifytoken', headers=headers) as response:
            print(f"Статус: {response.status}")
            response_text = await response.text()
            print(f"Тело ответа: {response_text}")


async def main():
    token = await test_auth_api()
    if token:
        await test_with_token(token)

asyncio.run(main())