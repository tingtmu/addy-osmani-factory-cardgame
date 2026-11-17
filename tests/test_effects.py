from typing import Any

import pytest

from cardengine.effects import CardDataError, parse_effect
from cardengine.loader import parse_card
from cardengine.models import Effect

CARD_ID = "card-under-test"


def test_damage_effect_parses() -> None:
    effect = parse_effect({"type": "damage", "amount": 6}, CARD_ID)

    assert effect == Effect(type="damage", params={"amount": 6})


def test_shield_effect_parses() -> None:
    effect = parse_effect({"type": "shield", "amount": 5}, CARD_ID)

    assert effect == Effect(type="shield", params={"amount": 5})


def test_draw_effect_parses() -> None:
    effect = parse_effect({"type": "draw", "amount": 2}, CARD_ID)

    assert effect == Effect(type="draw", params={"amount": 2})


def test_apply_status_effect_parses_without_optional_duration() -> None:
    effect = parse_effect({"type": "apply_status", "status": "poison", "stacks": 3}, CARD_ID)

    assert effect == Effect(type="apply_status", params={"status": "poison", "stacks": 3})


def test_apply_status_effect_parses_with_optional_duration() -> None:
    effect = parse_effect(
        {"type": "apply_status", "status": "poison", "stacks": 3, "duration": 4}, CARD_ID
    )

    assert effect == Effect(
        type="apply_status", params={"status": "poison", "stacks": 3, "duration": 4}
    )


def _assert_rejected(raw: dict[str, Any], *fragments: str) -> None:
    with pytest.raises(CardDataError) as excinfo:
        parse_effect(raw, CARD_ID)
    message = str(excinfo.value)
    assert CARD_ID in message
    for fragment in fragments:
        assert fragment in message


def test_missing_type_is_rejected() -> None:
    _assert_rejected({"amount": 6}, "type")


def test_non_string_type_is_rejected() -> None:
    _assert_rejected({"type": 7, "amount": 6}, "type")


def test_unknown_type_is_rejected() -> None:
    _assert_rejected({"type": "explode", "amount": 6}, "explode")


def test_missing_required_field_is_rejected() -> None:
    _assert_rejected({"type": "damage"}, "amount")


def test_missing_required_field_on_apply_status_is_rejected() -> None:
    _assert_rejected({"type": "apply_status", "stacks": 2}, "status")


def test_unknown_extra_field_is_rejected() -> None:
    _assert_rejected({"type": "damage", "amount": 6, "bonus": 1}, "bonus")


def test_non_positive_int_is_rejected() -> None:
    _assert_rejected({"type": "damage", "amount": 0}, "amount")


def test_negative_int_is_rejected() -> None:
    _assert_rejected({"type": "shield", "amount": -1}, "amount")


def test_string_amount_is_rejected() -> None:
    _assert_rejected({"type": "damage", "amount": "6"}, "amount")


def test_bool_amount_is_rejected() -> None:
    _assert_rejected({"type": "damage", "amount": True}, "amount")


def test_bool_stacks_is_rejected() -> None:
    _assert_rejected({"type": "apply_status", "status": "poison", "stacks": True}, "stacks")


def test_bool_duration_is_rejected() -> None:
    _assert_rejected(
        {"type": "apply_status", "status": "poison", "stacks": 1, "duration": False},
        "duration",
    )


def test_empty_status_is_rejected() -> None:
    _assert_rejected({"type": "apply_status", "status": "", "stacks": 1}, "status")


def test_parse_card_with_invalid_effect_raises_with_card_id() -> None:
    raw: dict[str, Any] = {
        "id": "bad-card",
        "name": "Bad",
        "cost": 1,
        "effects": [{"type": "damage", "amount": -3}],
    }

    with pytest.raises(CardDataError) as excinfo:
        parse_card(raw)

    assert "bad-card" in str(excinfo.value)
