import sys
from pathlib import Path

import pytest

from src.main import main


def test_add_and_list(monkeypatch: pytest.MonkeyPatch,tmp_path: Path,capsys: pytest.CaptureFixture[str],) -> None:
    """Проверяет добавление и вывод детали через команды"""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        'argv',
        [
            'lab3',
            'add',
            '--identifier', '0017',
            '--name', 'Турбина s210',
            '--category', 'Двигатель',
            '--date', '12.03.2020',
            '--fabricator', 'МАИ',
            '--compatibility', 'Boeing 737',
        ],
    )
    main()
    assert 'Добавлена деталь с id 0017' in capsys.readouterr().out
    assert (tmp_path / 'catalog.json').exists()
    monkeypatch.setattr(sys, 'argv', ['lab3', 'list'])
    main()
    assert 'Турбина s210' in capsys.readouterr().out
