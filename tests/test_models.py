import copy
import dataclasses
import pickle

import pytest

from cardengine.models import Card, Effect, Status, Unit


def _card(card_id: str = "c1") -> Card:
    return Card(id=card_id, name="Card", cost=1, effects=())


def test_status_with_duration_none_is_permanent() -> None:
    status = Status(name="poison", stacks=2, duration=None)

    assert status.name == "poison"
    assert status.stacks == 2
    assert status.duration is None


def test_status_with_finite_duration() -> None:
    status = Status(name="burn", stacks=1, duration=3)

    assert status.duration == 3


def test_status_is_frozen() -> None:
    status = Status(name="burn", stacks=1, duration=3)

    with pytest.raises(dataclasses.FrozenInstanceError):
        status.stacks = 5  # type: ignore[misc]


def test_unit_zones_are_independent_between_instances() -> None:
    first = Unit(name="a", max_hp=10, hp=10, energy=3)
    second = Unit(name="b", max_hp=10, hp=10, energy=3)

    first.hand.append(_card("x"))

    assert len(first.hand) == 1
    assert second.hand == []


def test_unit_deck_and_discard_are_independent_between_instances() -> None:
    first = Unit(name="a", max_hp=10, hp=10, energy=3)
    second = Unit(name="b", max_hp=10, hp=10, energy=3)

    first.deck.append(_card("d"))
    first.discard.append(_card("e"))

    assert len(first.deck) == 1
    assert len(first.discard) == 1
    assert second.deck == []
    assert second.discard == []


def test_unit_zones_are_distinct_lists_within_one_unit() -> None:
    unit = Unit(name="a", max_hp=10, hp=10, energy=3)

    zones = [unit.deck, unit.hand, unit.discard]

    assert all(isinstance(zone, list) for zone in zones)
    assert unit.deck is not unit.hand
    assert unit.deck is not unit.discard
    assert unit.hand is not unit.discard


def test_card_is_frozen() -> None:
    card = _card()

    with pytest.raises(dataclasses.FrozenInstanceError):
        card.cost = 9  # type: ignore[misc]


def test_effect_is_frozen() -> None:
    effect = Effect(type="damage", params={"amount": 6})

    with pytest.raises(dataclasses.FrozenInstanceError):
        effect.type = "heal"  # type: ignore[misc]


def test_card_with_effect_survives_deepcopy_pickle_and_asdict() -> None:
    card = Card(
        id="c2",
        name="Strike",
        cost=1,
        effects=(Effect(type="damage", params={"amount": 6, "target": "enemy"}),),
    )

    assert copy.deepcopy(card) == card
    assert pickle.loads(pickle.dumps(card)) == card
    assert dataclasses.asdict(card) == {
        "id": "c2",
        "name": "Strike",
        "cost": 1,
        "effects": (
            {"type": "damage", "params": {"amount": 6, "target": "enemy"}},
        ),
    }
