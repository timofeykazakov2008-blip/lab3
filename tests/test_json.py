import json
from collections.abc import Callable
from dataclasses import asdict
from pathlib import Path

import pytest

from src.catalog import Catalog
from src.constants import CATALOG_FORMAT_VERSION
from src.errors import LegalJson, UnsupportedVersionError
from src.json import down, save
from src.product import AirDetail


def test_down_rejects_unsupported_version(catalog: Catalog,make_detail: Callable[..., AirDetail],tmp_path: Path,) -> None:
    """Проверяет ошибку версии и сохранность каталога"""
    detail = make_detail()
    catalog.add(detail)
    document = {
        'format_version': CATALOG_FORMAT_VERSION + 1,
        'details': [],
    }
    path = tmp_path / 'catalog.json'
    path.write_text(json.dumps(document), encoding='utf-8')
    with pytest.raises(UnsupportedVersionError):
        down(catalog, path)
    assert list(catalog) == [detail]


@pytest.mark.parametrize('field', ['identifier', 'name', 'category', 'date', 'fabricator', 'compatibility'])
@pytest.mark.parametrize('value', [None, 123])
def test_wrong_field_type(
    catalog: Catalog,
    make_detail: Callable[..., AirDetail],
    tmp_path: Path,
    field: str,
    value: object,
) -> None:
    """Проверяет неверный тип поля и сохранность каталога"""
    detail = make_detail(identifier='9000')
    catalog.add(detail)
    record = asdict(make_detail(identifier='1001'))
    invalid_record = asdict(make_detail(identifier='1002'))
    invalid_record[field] = value
    document = {
        'format_version': CATALOG_FORMAT_VERSION,
        'details': [record, invalid_record],
    }
    path = tmp_path / 'catalog.json'
    path.write_text(json.dumps(document), encoding='utf-8')
    with pytest.raises(LegalJson):
        down(catalog, path)
    assert list(catalog) == [detail]


def test_wrong_encoding(catalog: Catalog, tmp_path: Path) -> None:
    """Проверяет обработку неверной кодировки"""
    path = tmp_path / 'catalog.json'
    path.write_bytes(b'\xff')
    with pytest.raises(LegalJson):
        down(catalog, path)


def test_save_and_down(catalog: Catalog, make_detail: Callable[..., AirDetail], tmp_path: Path) -> None:
    """Проверяет сохранение и загрузку всех полей"""
    first = make_detail(identifier='0017')
    second = make_detail(identifier='0018', name='Шасси', category='Шасси')
    catalog.add(first)
    catalog.add(second)
    path = tmp_path / 'catalog.json'
    save(catalog, path)
    document = json.loads(path.read_text(encoding='utf-8'))
    assert document['format_version'] == CATALOG_FORMAT_VERSION
    assert document['details'] == [asdict(first), asdict(second)]
    restored = Catalog()
    down(restored, path)
    assert list(restored) == [first, second]


def test_broken_json(catalog: Catalog, tmp_path: Path) -> None:
    """Проверяет обработку повреждённого JSON"""
    path = tmp_path / 'catalog.json'
    path.write_text('{broken', encoding='utf-8')
    with pytest.raises(LegalJson):
        down(catalog, path)
