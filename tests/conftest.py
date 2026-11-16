from collections.abc import Callable

import pytest

from src.catalog import Catalog
from src.product import AirDetail


@pytest.fixture
def make_detail() -> Callable[..., AirDetail]:
    """Даёт тестам функцию создания детали"""
    def create_detail(
        identifier: str = '0017',
        name: str = 'Турбина s210',
        category: str = 'Двигатель',
        date: str = '12.03.2020',
        fabricator: str = 'МАИ',
        compatibility: str = 'Boeing 737',
    ) -> AirDetail:
        """Создаёт деталь с указанными полями"""
        return AirDetail(
            identifier=identifier,
            name=name,
            category=category,
            date=date,
            fabricator=fabricator,
            compatibility=compatibility,
        )
    return create_detail

@pytest.fixture
def catalog() -> Catalog:
    """Создаёт пустой каталог для теста"""
    return Catalog()
