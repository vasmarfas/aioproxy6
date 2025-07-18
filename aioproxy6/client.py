import aiohttp
import asyncio
import time
from typing import Optional, List, Dict, Any, Union
from enum import Enum

from .models import (
    ProxyInfo, ProxyList, CountryList, CountInfo, 
    PriceInfo, ProlongProxyInfo, ProlongResult, 
    BuyResult, DeleteResult, CheckResult, ApiResponse
)


class ProxyVersion(Enum):
    """Версии прокси"""
    IPV4 = "4"
    IPV4_SHARED = "3"
    IPV6 = "6"


class ProxyType(Enum):
    """Типы прокси"""
    HTTP = "http"
    SOCKS = "socks"


class ProxyState(Enum):
    """Состояния прокси"""
    ACTIVE = "active"
    EXPIRED = "expired"
    EXPIRING = "expiring"
    ALL = "all"


class PX6Exception(Exception):
    """Исключение при работе с API px6.link"""
    
    def __init__(self, error_id: int, error_message: str):
        self.error_id = error_id
        self.error_message = error_message
        super().__init__(f"Error {error_id}: {error_message}")


class PX6Client:
    """Клиент для работы с API px6.link"""

    BASE_URL = "https://px6.link/api"

    def __init__(self, api_key: str, session: Optional[aiohttp.ClientSession] = None):
        """
        Инициализация клиента

        Args:
            api_key: API ключ
            session: Сессия aiohttp (если None, будет создана новая)

        """
        self.api_key = api_key
        self._session = session
        self._own_session = session is None

    async def __aenter__(self):
        if self._own_session:
            self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._own_session and self._session:
            await self._session.close()

    async def _request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Выполнение запроса к API

        Args:
            method: Метод API
            params: Параметры запроса

        Returns:
            Ответ API в виде словаря

        Raises:
            PX6Exception: Если API вернул ошибку
        """
        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._own_session = True

        # Формируем URL согласно документации: https://px6.link/api/{api_key}?method={method}&{params}
        url = f"{self.BASE_URL}/{self.api_key}/{method}"

        # all_params = {"method": method}
        # if params:
        #     all_params.update(params)

        async with self._session.get(url, params=params) as response:
            data = await response.json()

            if data.get("status") == "no":
                error_id = int(data.get("error_id", 0))
                error = data.get("error", "Unknown error")
                raise PX6Exception(error_id, error)

            return data

    async def get_price(self, count: int, period: int, version: ProxyVersion = ProxyVersion.IPV6) -> PriceInfo:
        """
        Получение стоимости заказа
        
        Args:
            count: Количество прокси
            period: Период действия (в днях)
            version: Версия прокси
            
        Returns:
            Информация о стоимости заказа
        """
        params = {
            "count": count,
            "period": period,
            "version": version.value
        }
        
        data = await self._request("getprice", params)
        return PriceInfo.from_dict(data)
    
    async def get_count(self, country: str, version: ProxyVersion = ProxyVersion.IPV6) -> CountInfo:
        """
        Получение количества доступных прокси в стране
        
        Args:
            country: Код страны (ru, ua, us и т.д.)
            version: Версия прокси
            
        Returns:
            Информация о доступном количестве прокси
        """
        params = {
            "country": country,
            "version": version.value
        }
        
        data = await self._request("getcountry", params)
        return CountInfo.from_dict(data)
    
    async def get_countries(self, version: ProxyVersion = ProxyVersion.IPV6) -> CountryList:
        """
        Получение списка доступных стран
        
        Args:
            version: Версия прокси
            
        Returns:
            Список доступных стран
        """
        params = {"version": version.value}
        
        data = await self._request("getcountries", params)
        return CountryList.from_dict(data)
    
    async def get_proxies(self,
                          state: ProxyState = ProxyState.ALL,
                          descr: Optional[str] = None,
                          nokey: bool = False,
                          page: int = 1,
                          limit: int = 1000) -> ProxyList:
        """
        Получение списка прокси
        
        Args:
            state: Состояние прокси (active, expired, expiring, all)
            descr: Фильтр по описанию
            nokey: Не возвращать ключи в ответе
            page: Номер страницы
            limit: Количество записей на странице
            
        Returns:
            Список прокси
        """
        params = {
            "state": state.value,
            "page": page,
            "limit": limit
        }
        
        if descr:
            params["descr"] = descr
            
        if nokey:
            params["nokey"] = 1
            
        data = await self._request("getproxy", params)
        return ProxyList.from_dict(data)
    
    async def set_proxy_type(self, proxy_ids: List[int], proxy_type: ProxyType) -> ApiResponse:
        """
        Установка типа прокси
        
        Args:
            proxy_ids: Список ID прокси
            proxy_type: Тип прокси (http, socks)
            
        Returns:
            Базовый ответ API
        """
        params = {
            "ids": ",".join(map(str, proxy_ids)),
            "type": proxy_type.value
        }
        
        data = await self._request("settype", params)
        return ApiResponse.from_dict(data)
    
    async def set_description(self, new_descr: str,
                              old_descr: Optional[str] = None,
                              proxy_ids: Optional[List[int]] = None) -> ApiResponse:
        """
        Установка описания для прокси
        
        Args:
            new_descr: Новое описание
            old_descr: Старое описание (для фильтрации)
            proxy_ids: Список ID прокси
            
        Returns:
            Базовый ответ API
        """
        params = {"new": new_descr}
        
        if old_descr:
            params["old"] = old_descr
            
        if proxy_ids:
            params["ids"] = ",".join(map(str, proxy_ids))
            
        data = await self._request("setdescr", params)
        return ApiResponse.from_dict(data)
    
    async def buy_proxies(self,
                          count: int,
                          period: int,
                          country: str,
                          version: ProxyVersion = ProxyVersion.IPV6,
                          proxy_type: ProxyType = ProxyType.HTTP,
                          descr: Optional[str] = None,
                          auto_prolong: bool = False,
                          nokey: bool = False) -> BuyResult:
        """
        Покупка прокси
        
        Args:
            count: Количество прокси
            period: Период действия (в днях)
            country: Код страны (ru, ua, us и т.д.)
            version: Версия прокси
            proxy_type: Тип прокси (http, socks)
            descr: Описание
            auto_prolong: Автоматическое продление
            nokey: Не возвращать ключи в ответе
            
        Returns:
            Результат покупки прокси
        """
        params = {
            "count": count,
            "period": period,
            "country": country,
            "version": version.value,
            "type": proxy_type.value
        }
        
        if descr:
            params["descr"] = descr
            
        if auto_prolong:
            params["auto_prolong"] = 1
            
        if nokey:
            params["nokey"] = 1
            
        data = await self._request("buy", params)
        return BuyResult.from_dict(data)
    
    async def prolong_proxies(self, proxy_ids: List[int], period: int, nokey: bool = False) -> ProlongResult:
        """
        Продление прокси
        
        Args:
            proxy_ids: Список ID прокси
            period: Период продления (в днях)
            nokey: Не возвращать ключи в ответе
            
        Returns:
            Результат продления прокси
        """
        params = {
            "ids": ",".join(map(str, proxy_ids)),
            "period": period
        }
        
        if nokey:
            params["nokey"] = 1
            
        data = await self._request("prolong", params)
        return ProlongResult.from_dict(data)
    
    async def delete_proxies(self, proxy_ids: Optional[List[int]] = None, descr: Optional[str] = None) -> DeleteResult:
        """
        Удаление прокси
        
        Args:
            proxy_ids: Список ID прокси
            descr: Фильтр по описанию
            
        Returns:
            Результат удаления прокси
        """
        params = {}
        
        if proxy_ids:
            params["ids"] = ",".join(map(str, proxy_ids))
            
        if descr:
            params["descr"] = descr
            
        data = await self._request("delete", params)
        return DeleteResult.from_dict(data)
    
    async def check_proxy(self, proxy_id: int) -> CheckResult:
        """
        Проверка прокси
        
        Args:
            proxy_id: ID прокси
            
        Returns:
            Результат проверки прокси
        """
        params = {"ids": str(proxy_id)}
        
        data = await self._request("check", params)
        return CheckResult.from_dict(data)
    
    async def set_ip_auth(self, ip_addresses: Union[List[str], str]) -> ApiResponse:
        """
        Установка IP-авторизации
        
        Args:
            ip_addresses: IP-адрес или список IP-адресов
            
        Returns:
            Базовый ответ API
        """
        if isinstance(ip_addresses, list):
            ip_param = ",".join(ip_addresses)
        else:
            ip_param = ip_addresses
            
        params = {"ip": ip_param}
        
        data = await self._request("ipauth", params)
        return ApiResponse.from_dict(data)
    
    async def remove_ip_auth(self) -> ApiResponse:
        """
        Удаление IP-авторизации
        
        Returns:
            Базовый ответ API
        """
        data = await self._request("ipauth", {"ip": "remove"})
        return ApiResponse.from_dict(data)
    
    async def get_balance(self) -> ApiResponse:
        """
        Получение баланса
        
        Returns:
            Базовый ответ API с информацией о балансе
        """
        data = await self._request("getbalance")
        return ApiResponse.from_dict(data) 