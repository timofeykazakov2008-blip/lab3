# Лабораторная работа 3: Каталог авиационных деталей
## Описание проекта

Программа представляет собой каталог авиационных деталей. Она позволяет добавлять и удалять детали, получать их по идентификатору, искать по названию и категории, а также сохранять каталог в JSON-файл и загружать его.

Каждая деталь содержит:
- числовой идентификатор;
- название;
- категорию;
- дату;
- производителя;
- совместимые модели самолётов.
## Структура проекта

```text
lab3/
├── README.md                   # Описание проекта и инструкция по запуску
├── pyproject.toml              # Настройки проекта и зависимости
├── requirements.txt            # Зависимости для стандартного venv
├── .gitignore                  # Файлы, исключённые из Git
├── .pre-commit-config.yaml     # Настройки проверок перед коммитом
├── src/
│   ├── __init__.py             # Инициализация пакета
│   ├── main.py                 # Точка входа и команды консольного интерфейса
│   ├── product.py              # Класс авиационной детали
│   ├── catalog.py              # Класс каталога и операции с деталями
│   ├── json.py                 # Сохранение и загрузка каталога в JSON
│   ├── errors.py               # Ошибкр приложения
│   └── constants.py            # Константы проекта
└── tests/
    ├── __init__.py
    ├── conftest.py             # Общие структуры для тестов
    ├── test_product.py         # Тесты создания и проверки детали
    ├── test_catalog.py         # Тесты операций каталога
    ├── test_errors.py          # Тесты ошибок
    ├── test_json.py            # Тесты сохранения и загрузки JSON
    └── test_main.py            # Тесты консольного интерфейса
```

## Установка
```bash
python3.12 -m venv .venv
source .venv/bin/activate
```
Установка инструментов для проверки:
```bash
python -m pip install pytest ruff mypy pre-commit
```

## Использование консольного интерфейса

Посмотреть доступные команды:
```bash
python -m src.main --help
```
Посмотреть аргументы команды добавления:
```bash
python -m src.main add --help
```
Добавить деталь:
```bash
python -m src.main add \
  --identifier 0017 \
  --name "Турбина s210" \
  --category "Двигатель" \
  --date 12.03.2020 \
  --fabricator "МАИ" \
  --compatibility "Boeing 737"
```
Показать все детали:
```bash
python -m src.main list
```
Получить деталь по ID:
```bash
python -m src.main get --identifier 0017
```
Найти детали по категории:
```bash
python -m src.main find_by_category --category "Двигатель"
```
Найти детали по названию:
```bash
python -m src.main find_by_name --name "турбина s210"
```
Показать количество деталей:
```bash
python -m src.main count
```
Удалить деталь по ID:
```bash
python -m src.main remove --identifier 0017
```
## Проверка проекта
```bash
python -m pytest -v
python -m pip install pytest-cov
python -m pytest --cov=src --cov-report=term-missing
```

```bash
ruff check .
mypy src/
```
