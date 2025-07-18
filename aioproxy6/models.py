from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum


@dataclass
class ProxyInfo:
    """Информация о прокси"""
    id: int
    ip: str
    host: str
    port: str
    user: str
    password: str
    type: str
    country: str
    date: str
    date_end: str
    unixtime: int
    unixtime_end: int
    descr: str
    active: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProxyInfo':
        """Создание объекта из словаря"""
        return cls(
            id=int(data.get('id', 0)),
            ip=data.get('ip', ''),
            host=data.get('host', ''),
            port=data.get('port', ''),
            user=data.get('user', ''),
            password=data.get('pass', ''),
            type=data.get('type', ''),
            country=data.get('country', ''),
            date=data.get('date', ''),
            date_end=data.get('date_end', ''),
            unixtime=int(data.get('unixtime', 0)),
            unixtime_end=int(data.get('unixtime_end', 0)),
            descr=data.get('descr', ''),
            active=data.get('active', '0') == '1'
        )


@dataclass
class ProxyList:
    """Список прокси"""
    status: str
    user_id: int
    balance: float
    currency: str
    list_count: int
    proxies_list: List[ProxyInfo]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProxyList':
        """Создание объекта из словаря"""
        proxies = []
        proxy_list = data.get('list', {})
        
        # Обработка списка с ключами и без ключей
        if isinstance(proxy_list, dict):
            for proxy_data in proxy_list.values():
                proxies.append(ProxyInfo.from_dict(proxy_data))
        elif isinstance(proxy_list, list):
            for proxy_data in proxy_list:
                proxies.append(ProxyInfo.from_dict(proxy_data))
        
        return cls(
            status=data.get('status', ''),
            user_id=int(data.get('user_id', 0)),
            balance=float(data.get('balance', 0)),
            currency=data.get('currency', ''),
            list_count=int(data.get('list_count', 0)),
            proxies_list=proxies
        )


@dataclass
class CountryList:
    """Список доступных стран"""
    status: str
    user_id: int
    balance: float
    currency: str
    countries: List[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CountryList':
        """Создание объекта из словаря"""
        return cls(
            status=data.get('status', ''),
            user_id=int(data.get('user_id', 0)),
            balance=float(data.get('balance', 0)),
            currency=data.get('currency', ''),
            countries=data.get('list', [])
        )


@dataclass
class CountInfo:
    """Информация о доступном количестве прокси"""
    status: str
    user_id: int
    balance: float
    currency: str
    count: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CountInfo':
        """Создание объекта из словаря"""
        return cls(
            status=data.get('status', ''),
            user_id=int(data.get('user_id', 0)),
            balance=float(data.get('balance', 0)),
            currency=data.get('currency', ''),
            count=int(data.get('count', 0))
        )


@dataclass
class PriceInfo:
    """Информация о стоимости заказа"""
    status: str
    user_id: int
    balance: float
    currency: str
    price: float
    price_single: float
    period: int
    count: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PriceInfo':
        """Создание объекта из словаря"""
        return cls(
            status=data.get('status', ''),
            user_id=int(data.get('user_id', 0)),
            balance=float(data.get('balance', 0)),
            currency=data.get('currency', ''),
            price=float(data.get('price', 0)),
            price_single=float(data.get('price_single', 0)),
            period=int(data.get('period', 0)),
            count=int(data.get('count', 0))
        )


@dataclass
class ProlongProxyInfo:
    """Информация о продленном прокси"""
    id: int
    date_end: str
    unixtime_end: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProlongProxyInfo':
        """Создание объекта из словаря"""
        return cls(
            id=int(data.get('id', 0)),
            date_end=data.get('date_end', ''),
            unixtime_end=int(data.get('unixtime_end', 0))
        )


@dataclass
class ProlongResult:
    """Результат продления прокси"""
    status: str
    user_id: int
    balance: float
    currency: str
    price: float
    period: int
    count: int
    proxies: List[ProlongProxyInfo]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProlongResult':
        """Создание объекта из словаря"""
        proxies = []
        proxy_list = data.get('list', {})
        
        # Обработка списка с ключами и без ключей
        if isinstance(proxy_list, dict):
            for proxy_data in proxy_list.values():
                proxies.append(ProlongProxyInfo.from_dict(proxy_data))
        elif isinstance(proxy_list, list):
            for proxy_data in proxy_list:
                proxies.append(ProlongProxyInfo.from_dict(proxy_data))
        
        return cls(
            status=data.get('status', ''),
            user_id=int(data.get('user_id', 0)),
            balance=float(data.get('balance', 0)),
            currency=data.get('currency', ''),
            price=float(data.get('price', 0)),
            period=int(data.get('period', 0)),
            count=int(data.get('count', 0)),
            proxies=proxies
        )


@dataclass
class BuyResult:
    """Результат покупки прокси"""
    status: str
    user_id: int
    balance: float
    currency: str
    count: int
    price: float
    period: int
    country: str
    proxies_list: List[ProxyInfo]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BuyResult':
        """Создание объекта из словаря"""
        proxies = []
        proxy_list = data.get('list', {})
        
        # Обработка списка с ключами и без ключей
        if isinstance(proxy_list, dict):
            for proxy_data in proxy_list.values():
                proxies.append(ProxyInfo.from_dict(proxy_data))
        elif isinstance(proxy_list, list):
            for proxy_data in proxy_list:
                proxies.append(ProxyInfo.from_dict(proxy_data))
        
        return cls(
            status=data.get('status', ''),
            user_id=int(data.get('user_id', 0)),
            balance=float(data.get('balance', 0)),
            currency=data.get('currency', ''),
            count=int(data.get('count', 0)),
            price=float(data.get('price', 0)),
            period=int(data.get('period', 0)),
            country=data.get('country', ''),
            proxies_list=proxies
        )


@dataclass
class DeleteResult:
    """Результат удаления прокси"""
    status: str
    user_id: int
    balance: float
    currency: str
    count: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DeleteResult':
        """Создание объекта из словаря"""
        return cls(
            status=data.get('status', ''),
            user_id=int(data.get('user_id', 0)),
            balance=float(data.get('balance', 0)),
            currency=data.get('currency', ''),
            count=int(data.get('count', 0))
        )


@dataclass
class CheckResult:
    """Результат проверки прокси"""
    status: str
    user_id: int
    balance: float
    currency: str
    proxy_id: int
    proxy_status: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CheckResult':
        """Создание объекта из словаря"""
        return cls(
            status=data.get('status', ''),
            user_id=int(data.get('user_id', 0)),
            balance=float(data.get('balance', 0)),
            currency=data.get('currency', ''),
            proxy_id=int(data.get('proxy_id', 0)),
            proxy_status=data.get('proxy_status', False)
        )


@dataclass
class ApiResponse:
    """Базовый ответ API"""
    status: str
    user_id: int
    balance: float
    currency: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ApiResponse':
        """Создание объекта из словаря"""
        return cls(
            status=data.get('status', ''),
            user_id=int(data.get('user_id', 0)),
            balance=float(data.get('balance', 0)),
            currency=data.get('currency', '')
        ) 