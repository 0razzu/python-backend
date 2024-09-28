from dataclasses import dataclass
from typing import ClassVar

from pydantic import BaseModel, ConfigDict


@dataclass(slots=True)
class CreateItemRequest:
    name: str
    price: float


class ModifyItemRequest(BaseModel):
    name: str | None = None
    price: float | None = None

    model_config = ConfigDict(extra='forbid')
