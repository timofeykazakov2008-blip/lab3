import json
from dataclasses import asdict
from pathlib import Path

from src.catalog import Catalog
from src.constants import CATALOG_FORMAT_VERSION
from src.errors import (
    DublErrors,
    FileErrors,
    LegalJson,
    ProductErrors,
    TimeErrors,
)
from src.product import AirDetail


def save(catalog: Catalog, path: str | Path) -> None:
    doc = {
        "format_version": CATALOG_FORMAT_VERSION,
        "details": [asdict(detail) for detail in catalog]
    }

    try:
        with Path(path).open('w', encoding = 'utf-8') as file:
            json.dump(doc, file, ensure_ascii=False, indent=2)
    except OSError as error:
        raise FileErrors ('Не удалось сохранить файл') from error

def down(catalog : Catalog, path: str | Path) -> None:
    try:
        with Path(path).open('r', encoding = 'utf-8') as file_json:
            file = json.load(file_json)
    except OSError as error:
        raise FileErrors ('Не удалось прочитать файл') from error
    except json.JSONDecodeError as error:
        raise LegalJson ('Поврежденный файл json') from error

    if not isinstance(file, dict):
        raise LegalJson('JSON должен быть объектом')

    version = file.get('format_version')
    if type(version) is not int:
        raise LegalJson('В файле отсутствует корректная версия')
    if version != CATALOG_FORMAT_VERSION:
        raise LegalJson('Версия файла не поддерживается')

    details = file.get('details')
    if not isinstance(details, list):
        raise LegalJson('Поле details должно быть списком')

    new_catalog = Catalog()
    for i, detail in enumerate(details):
        if not isinstance(detail, dict):
            raise LegalJson('запись детали с индексом должна быть объектом')
        try:
            product = AirDetail(**detail)
        except (TypeError, ProductErrors, TimeErrors) as error:
            raise LegalJson(f'Некорректный данные детали {i}') from error
        try:
            new_catalog.add(product)
        except DublErrors as error:
            raise LegalJson('ID детали повторяется') from error
    catalog.details = new_catalog.details
