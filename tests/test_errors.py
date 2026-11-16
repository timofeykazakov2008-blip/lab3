import pytest

from src.errors import (
    CatalogError,
    DublErrors,
    FileErrors,
    LegalJson,
    NonObjectErrors,
    ProductErrors,
    TimeErrors,
    UnsupportedVersionError,
)


@pytest.mark.parametrize(
    'error_type',
    [
        DublErrors,
        FileErrors,
        LegalJson,
        NonObjectErrors,
        ProductErrors,
        TimeErrors,
        UnsupportedVersionError,
    ],
)
def test_error_inherits_from_catalog_error(error_type: type[CatalogError]) -> None:
    """Проверяет общий базовый класс ошибок"""
    assert issubclass(error_type, CatalogError)

def test_legal_json_inherits_from_file_errors() -> None:
    """Проверяет, что ошибка JSON относится к ошибкам файла"""
    assert issubclass(LegalJson, FileErrors)
