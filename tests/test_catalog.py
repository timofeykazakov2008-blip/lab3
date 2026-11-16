from collections.abc import Callable

import pytest

from src.catalog import Catalog
from src.errors import DublErrors, NonObjectErrors
from src.product import AirDetail


def test_add_and_get(catalog: Catalog,make_detail: Callable[..., AirDetail]) -> None:
    """Проверяет добавление и получение детали"""
    detail = make_detail()
    catalog.add(detail)
    assert catalog.get('0017') is detail

def test_duplicate_identifier(catalog: Catalog,make_detail: Callable[..., AirDetail]) -> None:
    """Проверяет запрет одинаковых ID"""
    catalog.add(make_detail(identifier='0017'))
    with pytest.raises(DublErrors):
        catalog.add(make_detail(identifier='0017', name='Другая деталь'))
    assert len(catalog) == 1

def test_get_unknown_identifier(catalog: Catalog) -> None:
    """Проверяет получение несуществующей детали"""
    with pytest.raises(NonObjectErrors):
        catalog.get('404')

def test_remove(catalog: Catalog,make_detail: Callable[..., AirDetail]) -> None:
    """Проверяет удаление детали"""
    catalog.add(make_detail())
    catalog.remove('0017')
    assert len(catalog) == 0
    assert '0017' not in catalog
    with pytest.raises(NonObjectErrors):
        catalog.get('0017')

def test_remove_unknown_identifier(catalog: Catalog) -> None:
    """Проверяет удаление несуществующей детали"""
    with pytest.raises(NonObjectErrors):
        catalog.remove('404')


def test_find_by_category(catalog: Catalog,make_detail: Callable[..., AirDetail]) -> None:
    """Проверяет поиск по категории"""
    first = make_detail(identifier='0017', category='Двигатель')
    second = make_detail(identifier='0018', category='Крыло')
    catalog.add(first)
    catalog.add(second)
    assert catalog.find_by_category(' Двигатель ') == [first]
    assert catalog.find_by_category('Шасси') == []

def test_find_by_name(catalog: Catalog,make_detail: Callable[..., AirDetail]) -> None:
    """Проверяет поиск имени без учёта регистра"""
    detail = make_detail(name='Турбина s210')
    catalog.add(detail)
    assert catalog.find_by_name(' турбина S210 ') == [detail]
    assert catalog.find_by_name('Несуществующая деталь') == []

def test_search_returns_separate_list(catalog: Catalog,make_detail: Callable[..., AirDetail],) -> None:
    """Проверяет, что изменение результата поиска не удаляет детали"""
    detail = make_detail()
    catalog.add(detail)
    names = catalog.find_by_name(detail.name)
    categories = catalog.find_by_category(detail.category)
    names.clear()
    categories.clear()
    assert len(catalog) == 1
    assert catalog.get('0017') is detail

def test_len_iter_contains(catalog: Catalog,make_detail: Callable[..., AirDetail],) -> None:
    """Проверяет длину, порядок перебора и поиск ID через in"""
    first = make_detail(identifier='0017')
    second = make_detail(identifier='0018', name='Шасси')
    catalog.add(first)
    catalog.add(second)
    assert len(catalog) == 2
    assert list(catalog) == [first, second]
    assert '0017' in catalog
    assert '404' not in catalog
