from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class Effect:
    type: str
    params: Mapping[str, int | str]


@dataclass(frozen=True)
class Card:
    id: str
    name: str
    cost: int
    effects: tuple[Effect, ...]
