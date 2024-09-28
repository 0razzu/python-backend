from dataclasses import dataclass


@dataclass(slots=True)
class Item:
    id: int | None
    name: str
    price: float
    deleted: bool


@dataclass(slots=True)
class PatchItemInfo:
    name: str | None = None
    price: float | None = None

    def __bool__(self) -> bool:
        return self.name is not None or self.price is not None


@dataclass(slots=True)
class Cart:
    id: int | None
    items: dict[Item, int]
