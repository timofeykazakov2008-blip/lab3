import argparse
import sys
from collections.abc import Iterable
from pathlib import Path

from src.catalog import Catalog
from src.errors import CatalogError
from src.json import down, save
from src.product import AirDetail


def crt_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description = 'Каталог деталей')
    commands = parser.add_subparsers(dest = 'command', required = True)
    commands.add_parser('list', help = 'Показывает все детали из каталога')

    add_parser = commands.add_parser('add', help = 'Добавляет деталь в каталог')
    add_parser.add_argument('--identifier', help = 'id детали', required = True)
    add_parser.add_argument('--name', help = 'имя детали', required = True)
    add_parser.add_argument('--category', help = 'категория детали', required = True)
    add_parser.add_argument('--date', help = 'дата изготовления детали', required = True)
    add_parser.add_argument('--fabricator', help = 'изготовитель детали', required = True)
    add_parser.add_argument('--compatibility', help = 'совместимость детали с моделями самолетов', required = True)

    get_parser = commands.add_parser('get', help = 'Получает детали по id')
    get_parser.add_argument('--identifier', help = 'id детали', required = True)

    remove_parser = commands.add_parser('remove', help = 'Удаляет деталь из каталога')
    remove_parser.add_argument('--identifier', help = 'id детали', required = True)

    find_by_category = commands.add_parser('find_by_category', help = 'Находит все детали из категории')
    find_by_category.add_argument('--category', help = 'категория детали', required = True)

    find_by_name = commands.add_parser('find_by_name', help = 'Находит все детали по имени')
    find_by_name.add_argument('--name', help = 'имя детали', required = True)

    commands.add_parser('count', help = 'количество деталей в каталоге')
    return parser

def write_details(details: Iterable[AirDetail]) -> None:
    product = list(details)
    if not product:
        sys.stdout.write('Деталей нет\n')
        return
    for detail in product:
        sys.stdout.write(f'{detail}\n')

def main() -> None:
    parser = crt_parser()
    arg = parser.parse_args()
    catalog = Catalog()
    catalog_file = Path('catalog.json')

    try:
        if catalog_file.exists():
            down(catalog, catalog_file)

        if arg.command == 'list':
            write_details(catalog)

        elif arg.command == 'count':
            sys.stdout.write(f'{len(catalog)}\n')

        elif arg.command == 'add':
            detail = AirDetail(
                identifier=arg.identifier,
                name=arg.name,
                category=arg.category,
                date=arg.date,
                fabricator=arg.fabricator,
                compatibility=arg.compatibility,
            )
            catalog.add(detail)
            save(catalog, catalog_file)
            sys.stdout.write(f'Добавлена деталь с id {detail.identifier}\n')

        elif arg.command == 'remove':
            catalog.remove(arg.identifier)
            save(catalog, catalog_file)
            sys.stdout.write(f'Убрана деталь с id {arg.identifier}\n')

        elif arg.command == 'get':
            detail = catalog.get(arg.identifier)
            write_details([detail])

        elif arg.command == 'find_by_category':
            write_details(catalog.find_by_category(arg.category))

        elif arg.command == 'find_by_name':
            write_details(catalog.find_by_name(arg.name))

    except CatalogError as error:
        sys.stderr.write(f'Ошибка: {error}\n')
        raise SystemExit(2) from None
if __name__ == "__main__":
    main()
