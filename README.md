# aioproxy6

Асинхронный клиент для API px6.link (proxy6.net) на Python.

## Установка

```bash
pip install aioproxy6
```

## Использование

### Базовый пример

```python
import asyncio
from aioproxy6 import PX6Client, ProxyVersion

async def main():
    # Создание клиента
    client = PX6Client(api_key="YOUR_API_KEY")
    
    # Получение баланса
    balance = await client.get_balance()
    print(f"Баланс: {balance.balance} {balance.currency}")
    
    # Получение списка прокси
    proxies = await client.get_proxies()
    print(f"Всего прокси: {proxies.list_count}")
    
    # Вывод информации о прокси
    for proxy in proxies.proxies_list:
        print(f"ID: {proxy.id}, IP: {proxy.ip}, Страна: {proxy.country}, Активен: {proxy.active}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Покупка прокси

```python
import asyncio
from aioproxy6 import PX6Client, ProxyVersion, ProxyType

async def buy_proxy():
    client = PX6Client(api_key="YOUR_API_KEY")
    
    # Получение списка доступных стран для IPv4 Shared
    countries = await client.get_countries(version=ProxyVersion.IPV4_SHARED)
    print(f"Доступные страны: {', '.join(countries.countries)}")
    
    # Проверка доступности прокси в России
    count_info = await client.get_count("ru", version=ProxyVersion.IPV4_SHARED)
    print(f"Доступно прокси в России: {count_info.count}")
    
    # Получение стоимости заказа
    price_info = await client.get_price(count=1, period=30, version=ProxyVersion.IPV4_SHARED)
    print(f"Стоимость: {price_info.price} {price_info.currency}")
    
    # Покупка прокси
    if count_info.count > 0:
        result = await client.buy_proxies(
            count=1,
            period=30,
            country="ru",
            version=ProxyVersion.IPV4_SHARED,
            proxy_type=ProxyType.HTTP,
            descr="Тестовый прокси"
        )
        
        for proxy in result.proxies_list:
            print(f"Куплен прокси: {proxy.host}:{proxy.port}")
            print(f"Логин: {proxy.user}")
            print(f"Пароль: {proxy.password}")
            print(f"Действует до: {proxy.date_end}")

if __name__ == "__main__":
    asyncio.run(buy_proxy())
```

### Продление прокси

```python
import asyncio
from aioproxy6 import PX6Client, ProxyState

async def prolong_proxies():
    client = PX6Client(api_key="YOUR_API_KEY")
    
    # Получение списка активных прокси
    proxies = await client.get_proxies(state=ProxyState.ACTIVE)
    
    if proxies.proxies_list:
        # Получение ID первого прокси
        proxy_id = proxies.proxies_list[0].id
        
        # Продление прокси на 7 дней
        result = await client.prolong_proxies([proxy_id], period=7)
        
        print(f"Прокси продлен до: {result.proxies[0].date_end}")
        print(f"Новый баланс: {result.balance} {result.currency}")

if __name__ == "__main__":
    asyncio.run(prolong_proxies())
```

### Использование контекстного менеджера

```python
import asyncio
from aioproxy6 import PX6Client

async def main():
    async with PX6Client(api_key="YOUR_API_KEY") as client:
        balance = await client.get_balance()
        print(f"Баланс: {balance.balance} {balance.currency}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Документация

### Классы и перечисления

- `PX6Client` - основной класс для работы с API
- `ProxyVersion` - перечисление версий прокси (IPV4, IPV4_SHARED, IPV6)
- `ProxyType` - перечисление типов прокси (HTTP, SOCKS)
- `ProxyState` - перечисление состояний прокси (ACTIVE, EXPIRED, EXPIRING, ALL)

### Методы PX6Client

- `get_balance()` - получение баланса
- `get_countries(version)` - получение списка доступных стран
- `get_count(country, version)` - получение количества доступных прокси в стране
- `get_price(count, period, version)` - получение стоимости заказа
- `get_proxies(state, descr, nokey, page, limit)` - получение списка прокси
- `buy_proxies(count, period, country, version, proxy_type, descr, auto_prolong, nokey)` - покупка прокси
- `prolong_proxies(proxy_ids, period, nokey)` - продление прокси
- `delete_proxies(proxy_ids, descr)` - удаление прокси
- `check_proxy(proxy_id)` - проверка прокси
- `set_proxy_type(proxy_ids, proxy_type)` - установка типа прокси
- `set_description(new_descr, old_descr, proxy_ids)` - установка описания для прокси
- `set_ip_auth(ip_addresses)` - установка IP-авторизации
- `remove_ip_auth()` - удаление IP-авторизации

## Лицензия

MIT 