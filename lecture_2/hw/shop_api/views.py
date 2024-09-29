from dataclasses import dataclass
from typing import Annotated

from lecture_2.hw.shop_api.models import Item


@dataclass(slots=True)
class CartView:
    id: int
    items: dict[Item, Annotated[int, 'Quantity']]
    price: float
    quantity: int

    def __repr__(self):
        return f'{self.id}'

    def __hash__(self):
        return hash(repr(self))