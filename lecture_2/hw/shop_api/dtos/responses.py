from dataclasses import dataclass


@dataclass(slots=True)
class ItemResponse:
    id: int
    name: str
    price: float


@dataclass(slots=True)
class ModifyItemResponse:
    id: int
    name: str | None
    price: float | None