from dataclasses import dataclass
from typing import Optional


@dataclass
class Player:
    """The player class."""

    name: str
    team: str
    number: int
    position: str
    age: int
    height: str
    weight: int
    college: Optional[str]  # None when the source cell is empty.
    salary: Optional[int]  # None when the source cell is empty.
