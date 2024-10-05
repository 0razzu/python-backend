from dataclasses import dataclass
from typing import Annotated

from fastapi.params import Query
from pydantic import BaseModel, ConfigDict

NameType = Annotated[str, Query(min_length=3)]


@dataclass(slots=True)
class CreateItemRequest:
    name: NameType
    price: float


class ModifyItemRequest(BaseModel):
    name: NameType | None = None
    price: float | None = None

    model_config = ConfigDict(extra='forbid')
