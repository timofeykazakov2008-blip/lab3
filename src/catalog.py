from collections.abc import Iterator

from src.errors import DublErrors, NonObjectErrors
from src.product import AirDetail


class Catalog:
    def __init__(self) -> None:
        self.details: dict[str, AirDetail] = {}

    def add(self, detail : AirDetail) -> None:
        if detail.identifier in self.details:
            raise DublErrors(f'Деталь с ID {detail.identifier} уже существует')
        self.details[detail.identifier] = detail

    def get(self, id : str) -> AirDetail:
        if id not in self.details:
            raise NonObjectErrors(f'Деталь с ID {id} не существует')
        return(self.details[id])

    def remove(self, id : str) -> None:
        if id not in self.details:
            raise NonObjectErrors(f'Деталь с ID {id} не существует')
        del self.details[id]

    def find_by_category(self, category : str) -> list[AirDetail]:
        match = []
        category = category.strip()
        for detail in self.details.values():
            if detail.category == category:
                match.append(detail)
        return match

    def find_by_name(self, name : str) -> list[AirDetail]:
        match = []
        for detail in self.details.values():
            if detail.name.casefold() == name.strip().casefold():
                match.append(detail)
        return match

    def __len__(self) -> int:
        return(len(self.details))

    def __iter__(self) -> Iterator[AirDetail]:
        return(iter(self.details.values()))

    def __contains__(self, id : str) -> bool:
        return id in self.details
