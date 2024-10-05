from dataclasses import dataclass


@dataclass(slots=True)
class ItemResponse:
    id: int
    name: str
    price: float


@dataclass(slots=True)
class GetItemsResponseItem:
    id: int
    name: str
    price: float
    available: bool


@dataclass(slots=True)
class ModifyItemResponse:
    id: int
    name: str | None
    price: float | None


@dataclass(slots=True)
class CreateCartResponse:
    id: int


@dataclass(slots=True)
class GetCartResponseItem:
    id: int
    name: str
    price: float
    quantity: int
    available: bool


@dataclass(slots=True)
class GetCartResponse:
    id: int
    items: list[GetCartResponseItem]
    price: float


@dataclass(slots=True)
class GetCartsResponseCart:
    id: int
    items: list[GetCartResponseItem]
    price: float
    quantity: int


@dataclass(slots=True)
class ErrorReason:
    loc: str
