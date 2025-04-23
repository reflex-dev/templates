from typing import (
    Literal,
    TypedDict,
)


class DetailEntry(TypedDict):
    id: int
    owner: str
    status: Literal["Live", "Inactive", "Archived"]
    region: str
    stability: int
    costs: float
    last_edited: str
