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
        headers = {'Client-Mobile': 'true'}
        
        async with session.post(f'{base_url}/register', json=register_data, headers=headers) as response:
            print(f"Статус: {response.status}")
            response_text = await response.text()
            print(f"Тело ответа: {response_text}")
            
            if response.status == 201:
                try:
                    response_data = json.loads(response_text)
                    access_token = response_data.get('access_token')
                    refresh_token = response_data.get('refresh_token')
                    print(f"✅ Регистрация успешна!")
                    print(f"Access Token получен: {bool(access_token)}")
                    print(f"Refresh Token получен: {bool(refresh_token)}")
                    return access_token, refresh_token
                except Exception as e:
                    print(f"❌ Ошибка парсинга токенов: {e}")
                    return None, None
            else:
                print("❌ Регистрация не удалась")
                return None, None
        
        print("\n=== ЛОГИН ===")
        login_data = {
            'username': 'Alice', 
            'password': '38752598y963896'
        }
        async with session.post(f'{base_url}/login', json=login_data, headers=headers) as response:
            print(f"Статус: {response.status}")
            response_text = await response.text()
            print(f"Тело ответа: {response_text}")
            
            if response.status == 200:
                try:
                    response_data = json.loads(response_text)
                    access_token = response_data.get('access_token')
                    refresh_token = response_data.get('refresh_token')
                    print(f"✅ Логин успешен!")
                    print(f"Access Token получен: {bool(access_token)}")
                    print(f"Refresh Token получен: {bool(refresh_token)}")
                    return access_token, refresh_token
                except Exception as e:
                    print(f"❌ Ошибка парсинга токенов: {e}")
                    return None, None
            else:
                print("❌ Логин не удался")
                return None, None

async def test_with_token(access_token, refresh_token):
    base_url = 'http://127.0.0.1:8000/v1/auth'
    
    async with aiohttp.ClientSession() as session:
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Client-Mobile': 'true'
        }
        
        print("\n=== ПРОВЕРКА ТОКЕНА ===")
        async with session.get(f'{base_url}/verifytoken', headers=headers) as response:
            print(f"Статус: {response.status}")
            response_text = await response.text()
            print(f"Тело ответа: {response_text}")

async def test_refresh_token(refresh_token):
    base_url = 'http://127.0.0.1:8000/v1/auth'
    
    async with aiohttp.ClientSession() as session:
        headers = {'Client-Mobile': 'true'}
        refresh_data = {'refresh_token': refresh_token}
        
        print("\n=== ОБНОВЛЕНИЕ ТОКЕНОВ ===")
        async with session.post(f'{base_url}/refresh', json=refresh_data, headers=headers) as response:
            print(f"Статус: {response.status}")
            response_text = await response.text()
            print(f"Тело ответа: {response_text}")
            
            if response.status == 200:
                try:
                    response_data = json.loads(response_text)
                    new_access_token = response_data.get('access_token')
                    new_refresh_token = response_data.get('refresh_token')
                    print(f"✅ Токены успешно обновлены!")
                    print(f"Новый Access Token получен: {bool(new_access_token)}")
                    print(f"Новый Refresh Token получен: {bool(new_refresh_token)}")
                    return new_access_token, new_refresh_token
                except Exception as e:
                    print(f"❌ Ошибка парсинга новых токенов: {e}")
                    return None, None
            else:
                print("❌ Обновление токенов не удалось")
                return None, None

async def test_logout(refresh_token):
    base_url = 'http://127.0.0.1:8000/v1/auth'
    
    async with aiohttp.ClientSession() as session:
        headers = {'Client-Mobile': 'true'}
        logout_data = {'refresh_token': refresh_token}
        
        print("\n=== ВЫХОД ИЗ СИСТЕМЫ ===")
        async with session.post(f'{base_url}/logout', json=logout_data, headers=headers) as response:
            print(f"Статус: {response.status}")
            response_text = await response.text()
            print(f"Тело ответа: {response_text}")
            
            if response.status == 200:
                print("✅ Выход выполнен успешно")
                return True
            else:
                print("❌ Выход не удался")
                return False

async def test_invalid_token():
    base_url = 'http://127.0.0.1:8000/v1/auth'
    
    async with aiohttp.ClientSession() as session:
        headers = {
            'Authorization': 'Bearer invalid_token_here',
            'Client-Mobile': 'true'
        }
        
        print("\n=== ПРОВЕРКА НЕВАЛИДНОГО ТОКЕНА ===")
        async with session.get(f'{base_url}/verifytoken', headers=headers) as response:
            print(f"Статус: {response.status}")
            response_text = await response.text()
            print(f"Тело ответа: {response_text}")

async def test_without_mobile_header():
    base_url = 'http://127.0.0.1:8000/v1/auth'
    
    async with aiohttp.ClientSession() as session:
        login_data = {
            'username': 'Alice', 
            'password': '38752598y963896'
        }
        
        print("\n=== ЛОГИН БЕЗ CLIENT-MOBILE HEADER ===")
        async with session.post(f'{base_url}/login', json=login_data) as response:
            print(f"Статус: {response.status}")
            response_text = await response.text()
            print(f"Тело ответа: {response_text}")

async def test_complete_flow():
    """Полный тест всего цикла аутентификации"""
    print("🚀 ЗАПУСК ПОЛНОГО ТЕСТА АУТЕНТИФИКАЦИИ")
    print("=" * 50)
    
    base_url = 'http://127.0.0.1:8000/v1/auth'
    headers = {'Client-Mobile': 'true'}
    
    async with aiohttp.ClientSession() as session:
        # 1. Регистрация
        print("\n1. 📝 РЕГИСТРАЦИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ")
        register_data = {
            'username': 'test_user_123', 
            'password': 'testpassword123', 
            'email': 'test123@mail.ru'
        }
        
        async with session.post(f'{base_url}/register', json=register_data, headers=headers) as response:
            if response.status == 201:
                response_data = await response.json()
                access_token_1 = response_data['access_token']
                refresh_token_1 = response_data['refresh_token']
                print("✅ Регистрация успешна")
            else:
                print("❌ Регистрация не удалась, пробуем логин")
                # Если пользователь уже существует, пробуем логин
                login_data = {
                    'username': 'test_user_123', 
                    'password': 'testpassword123'
                }
                async with session.post(f'{base_url}/login', json=login_data, headers=headers) as login_response:
                    if login_response.status == 200:
                        response_data = await login_response.json()
                        access_token_1 = response_data['access_token']
                        refresh_token_1 = response_data['refresh_token']
                        print("✅ Логин успешен")
                    else:
                        print("❌ Логин также не удался")
                        return
        
        # 2. Проверка токена
        print("\n2. 🔐 ПРОВЕРКА ВАЛИДНОСТИ ТОКЕНА")
        auth_headers = {'Authorization': f'Bearer {access_token_1}', 'Client-Mobile': 'true'}
        async with session.get(f'{base_url}/verifytoken', headers=auth_headers) as response:
            if response.status == 200:
                user_info = await response.json()
                print(f"✅ Токен валиден. Пользователь: {user_info['username']}")
            else:
                print("❌ Токен невалиден")
                return
        
        # 3. Обновление токенов
        print("\n3. 🔄 ОБНОВЛЕНИЕ ТОКЕНОВ")
        refresh_data = {'refresh_token': refresh_token_1}
        async with session.post(f'{base_url}/refresh', json=refresh_data, headers=headers) as response:
            if response.status == 200:
                response_data = await response.json()
                access_token_2 = response_data['access_token']
                refresh_token_2 = response_data['refresh_token']
                print("✅ Токены успешно обновлены")
            else:
                print("❌ Обновление токенов не удалось")
                return
        
        # 4. Проверка нового токена
        print("\n4. 🔐 ПРОВЕРКА НОВОГО ТОКЕНА")
        new_auth_headers = {'Authorization': f'Bearer {access_token_2}', 'Client-Mobile': 'true'}
        async with session.get(f'{base_url}/verifytoken', headers=new_auth_headers) as response:
            if response.status == 200:
                user_info = await response.json()
                print(f"✅ Новый токен валиден. Пользователь: {user_info['username']}")
            else:
                print("❌ Новый токен невалиден")
                return
        
        # 5. Выход из системы
        print("\n5. 🚪 ВЫХОД ИЗ СИСТЕМЫ")
        logout_data = {'refresh_token': refresh_token_2}
        async with session.post(f'{base_url}/logout', json=logout_data, headers=headers) as response:
            if response.status == 200:
                print("✅ Выход выполнен успешно")
            else:
                print("❌ Выход не удался")
        
        # 6. Попытка использовать старый refresh token после выхода
        print("\n6. ⚠️  ПРОВЕРКА BLACKLIST REFRESH TOKEN")
        async with session.post(f'{base_url}/refresh', json=logout_data, headers=headers) as response:
            if response.status == 401:
                print("✅ Refresh token правильно добавлен в blacklist")
            else:
                print("❌ Refresh token все еще работает после выхода")
        
        print("\n" + "=" * 50)
        print("🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО УСПЕШНО!")

async def main():
    # Запуск полного теста
    await test_complete_flow()

asyncio.run(main())