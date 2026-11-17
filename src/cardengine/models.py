from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType


@dataclass(frozen=True)
class Effect:
    type: str
    params: Mapping[str, int | str]

    def __post_init__(self) -> None:
        object.__setattr__(self, "params", MappingProxyType(dict(self.params)))


@dataclass(frozen=True)
class Card:
    id: str
    name: str
    cost: int
    effects: tuple[Effect, ...]


@dataclass(frozen=True)
class Status:
    """A status condition applied to a unit.

    ``duration`` is the number of turns the status lasts. ``None`` means the
    status is permanent and never expires on its own.
    """

    name: str
    stacks: int
    duration: int | None


@dataclass
class Unit:
    name: str
    max_hp: int
    hp: int
    energy: int
    deck: list[Card] = field(default_factory=list)
    hand: list[Card] = field(default_factory=list)
    discard: list[Card] = field(default_factory=list)
