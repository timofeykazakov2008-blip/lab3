from collections.abc import Callable
from dataclasses import FrozenInstanceError

import pytest

from src.errors import ProductErrors, TimeErrors
from src.product import AirDetail


def test_valid_data(make_detail: Callable[..., AirDetail]) -> None:
    """Проверяет создание детали с корректными данными"""
    detail = make_detail()

    assert detail.identifier == '0017'
    assert detail.name == 'Турбина s210'
    assert detail.category == 'Двигатель'
    assert detail.date == '12.03.2020'
    assert detail.fabricator == 'МАИ'
    assert detail.compatibility == 'Boeing 737'


def test_air_detail_strips(make_detail: Callable[..., AirDetail]) -> None:
    """Проверяет удаление пробелов и нормализацию даты"""
    detail = make_detail(
        identifier=' 0017 ',
        name=' Турбина s210 ',
        category=' Двигатель ',
        date='1.2.2024',
        fabricator=' МАИ ',
        compatibility=' Boeing 737 ',
    )

    assert detail.identifier == '0017'
    assert detail.name == 'Турбина s210'
    assert detail.category == 'Двигатель'
    assert detail.date == '01.02.2024'
    assert detail.fabricator == 'МАИ'
    assert detail.compatibility == 'Boeing 737'


@pytest.mark.parametrize('identifier', ['', '  ', 'abc', '17-2'])
def test_invalid_identifier(make_detail: Callable[..., AirDetail],identifier: str) -> None:
    """Проверяет отклонение неверного ID"""
    with pytest.raises(ProductErrors):
        make_detail(identifier=identifier)


@pytest.mark.parametrize('field',['name', 'category', 'fabricator', 'compatibility'])
def test_blank_field(make_detail: Callable[..., AirDetail],field: str) -> None:
    """Проверяет отклонение пустого текстового поля"""
    with pytest.raises(ProductErrors):
        make_detail(**{field: '   '})


def test_empty_date(make_detail: Callable[..., AirDetail]) -> None:
    """Проверяет отклонение пустой даты"""
    with pytest.raises(ProductErrors):
        make_detail(date='   ')


@pytest.mark.parametrize('date', ['31.02.2024', '2024-02-29'])
def test_invalid_date(make_detail: Callable[..., AirDetail],date: str) -> None:
    """Проверяет отклонение неверной даты"""
    with pytest.raises(TimeErrors):
        make_detail(date=date)

def test_detail_is_immutable(make_detail: Callable[..., AirDetail]) -> None:
    """Проверяет запрет изменения полей детали."""
    detail = make_detail()
    with pytest.raises(FrozenInstanceError):
        detail.identifier = '9999' # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        detail.name = 'Шасси' # type: ignore[misc]
