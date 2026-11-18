from collections.abc import Mapping
from dataclasses import dataclass, field


# Effect is frozen, so attribute reassignment is blocked. ``params`` is the
# caller's mapping and is not copied, so immutability is shallow: mutating the
# mapping the caller passed in will change the Effect.
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
