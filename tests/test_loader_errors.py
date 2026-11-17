import json
import re
from pathlib import Path

import pytest

from cardengine.effects import CardDataError
from cardengine.loader import load_cards, parse_card

CARD_ID = "bad-card"


def _card(**overrides: object) -> dict[str, object]:
    card: dict[str, object] = {
        "id": CARD_ID,
        "name": "Bad Card",
        "cost": 1,
        "effects": [{"type": "damage", "amount": 6}],
    }
    card.update(overrides)
    return card


def _without(key: str) -> dict[str, object]:
    card = _card()
    del card[key]
    return card


def _write(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "cards.json"
    path.write_text(text, encoding="utf-8")
    return path


def test_negative_cost_is_rejected() -> None:
    with pytest.raises(CardDataError, match=CARD_ID):
        parse_card(_card(cost=-1))


def test_bool_cost_is_rejected() -> None:
    with pytest.raises(CardDataError, match=CARD_ID):
        parse_card(_card(cost=True))


@pytest.mark.parametrize("cost", ["1", 1.5, None])
def test_non_int_cost_is_rejected(cost: object) -> None:
    with pytest.raises(CardDataError, match=CARD_ID):
        parse_card(_card(cost=cost))


def test_empty_effects_is_rejected() -> None:
    with pytest.raises(CardDataError, match=CARD_ID):
        parse_card(_card(effects=[]))


@pytest.mark.parametrize("effects", [{"type": "damage", "amount": 6}, 5, None])
def test_effects_not_a_list_is_rejected(effects: object) -> None:
    with pytest.raises(CardDataError, match=CARD_ID):
        parse_card(_card(effects=effects))


def test_missing_name_is_rejected() -> None:
    with pytest.raises(CardDataError, match="name"):
        parse_card(_without("name"))


def test_blank_name_is_rejected() -> None:
    with pytest.raises(CardDataError, match=CARD_ID):
        parse_card(_card(name="   "))


def test_missing_id_is_rejected() -> None:
    with pytest.raises(CardDataError, match="id"):
        parse_card(_without("id"))


def test_malformed_json_names_the_path(tmp_path: Path) -> None:
    path = _write(tmp_path, '{"cards": [')

    with pytest.raises(CardDataError, match=re.escape(str(path))):
        load_cards(path)


def test_invalid_utf8_names_the_path(tmp_path: Path) -> None:
    path = tmp_path / "cards.json"
    path.write_bytes(b'{"cards": []}\xff')

    with pytest.raises(CardDataError, match=re.escape(str(path))):
        load_cards(path)


def test_deeply_nested_json_names_the_path(tmp_path: Path) -> None:
    path = _write(tmp_path, "[" * 100000)

    with pytest.raises(CardDataError, match=re.escape(str(path))):
        load_cards(path)


def test_top_level_not_an_object_is_rejected(tmp_path: Path) -> None:
    path = _write(tmp_path, "[]")

    with pytest.raises(CardDataError, match=re.escape(str(path))):
        load_cards(path)


def test_cards_not_a_list_is_rejected(tmp_path: Path) -> None:
    path = _write(tmp_path, json.dumps({"cards": {"id": CARD_ID}}))

    with pytest.raises(CardDataError, match=re.escape(str(path))):
        load_cards(path)


def test_duplicate_card_ids_are_rejected(tmp_path: Path) -> None:
    payload = {"cards": [_card(id="dup"), _card(id="dup", name="Other")]}
    path = _write(tmp_path, json.dumps(payload))

    with pytest.raises(CardDataError, match="dup"):
        load_cards(path)


@pytest.mark.parametrize("entry", [5, None, "type"])
def test_non_mapping_effect_entry_is_rejected(entry: object) -> None:
    with pytest.raises(CardDataError, match=CARD_ID):
        parse_card(_card(effects=[entry]))


def test_whitespace_only_apply_status_is_rejected() -> None:
    effect = {"type": "apply_status", "status": "   ", "stacks": 1}

    with pytest.raises(CardDataError, match=CARD_ID):
        parse_card(_card(effects=[effect]))


def test_valid_file_still_loads(tmp_path: Path) -> None:
    payload = {"cards": [_card(id="strike", name="Strike", cost=1)]}
    path = _write(tmp_path, json.dumps(payload))

    cards = load_cards(path)

    assert set(cards) == {"strike"}
    assert cards["strike"].name == "Strike"
    assert cards["strike"].cost == 1
    assert dict(cards["strike"].effects[0].params) == {"amount": 6}
