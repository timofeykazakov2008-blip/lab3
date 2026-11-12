from dataclasses import dataclass
from datetime import datetime

from src.errors import ProductErrors, TimeErrors


@dataclass
class AirDetail:
    identifier: str
    name: str
    category: str
    date: str
    fabricator: str
    compatibility: str

    def __post_init__(self) -> None:
        self.identifier = self.identifier.strip()
        if self.identifier:
            if any(i not in "0123456789" for i in self.identifier):
                raise ProductErrors("ID должен состоять только из цифр")
        else:
            raise ProductErrors('ID не может быть пустым')

        self.name = self.name.strip()
        if not self.name:
            raise ProductErrors('Название не может быть пустым')

        self.category = self.category.strip()
        if not self.category:
            raise ProductErrors('Категория не может быть пустая')

        self.date = self.date.strip()
        if not self.date:
            raise ProductErrors('Дата не может быть пустой')
        try:
            date = datetime.strptime(self.date, "%d.%m.%Y")
        except ValueError as error:
            raise TimeErrors("Дата должна быть реальной и записанной в формате ДД.ММ.ГГГГ") from error
        self.date = date.strftime("%d.%m.%Y")

        self.fabricator = self.fabricator.strip()
        if not self.fabricator:
            raise ProductErrors('Производитель не может отсутствовать')

        self.compatibility = self.compatibility.strip()
        if not self.compatibility:
            raise ProductErrors('У детали должны быть совместивые модели')
