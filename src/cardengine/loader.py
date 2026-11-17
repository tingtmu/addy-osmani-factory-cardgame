import json
from collections.abc import Mapping
from pathlib import Path

from cardengine.effects import CardDataError, parse_effect
from cardengine.models import Card, Effect

__all__ = ["CardDataError", "load_cards", "parse_card"]

# Used in error messages until the card's own id has been validated.
_UNKNOWN_ID = "<unknown>"


def _require(raw: Mapping[str, object], field: str, card_id: str) -> object:
    if field not in raw:
        raise CardDataError(f"card {card_id}: missing required field {field!r}")
    return raw[field]


def _text(raw: Mapping[str, object], field: str, card_id: str) -> str:
    value = _require(raw, field, card_id)
    if not isinstance(value, str) or not value.strip():
        raise CardDataError(
            f"card {card_id}: field {field!r} must be a non-empty string, got {value!r}"
        )
    return value


def _cost(raw: Mapping[str, object], card_id: str) -> int:
    value = _require(raw, "cost", card_id)
    # bool is a subclass of int in Python, so it must be excluded explicitly.
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise CardDataError(f"card {card_id}: field 'cost' must be an integer >= 0, got {value!r}")
    return value


def _effects(raw: Mapping[str, object], card_id: str) -> tuple[Effect, ...]:
    value = _require(raw, "effects", card_id)
    if not isinstance(value, list) or not value:
        raise CardDataError(
            f"card {card_id}: field 'effects' must be a non-empty list, got {value!r}"
        )
    effects: list[Effect] = []
    for entry in value:
        if not isinstance(entry, Mapping):
            raise CardDataError(f"card {card_id}: each effect must be an object, got {entry!r}")
        effects.append(parse_effect(entry, card_id))
    return tuple(effects)


def parse_card(raw: Mapping[str, object]) -> Card:
    card_id = _text(raw, "id", _UNKNOWN_ID)
    return Card(
        id=card_id,
        name=_text(raw, "name", card_id),
        cost=_cost(raw, card_id),
        effects=_effects(raw, card_id),
    )


def load_cards(path: Path) -> dict[str, Card]:
    with path.open(encoding="utf-8") as handle:
        try:
            data: object = json.load(handle)
        except json.JSONDecodeError as exc:
            raise CardDataError(f"{path}: malformed JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise CardDataError(f"{path}: top-level JSON must be an object with a 'cards' list")
    raw_cards = data.get("cards")
    if not isinstance(raw_cards, list):
        raise CardDataError(f"{path}: field 'cards' must be a list")

    cards: dict[str, Card] = {}
    for raw in raw_cards:
        if not isinstance(raw, Mapping):
            raise CardDataError(f"{path}: each entry in 'cards' must be an object, got {raw!r}")
        card = parse_card(raw)
        if card.id in cards:
            raise CardDataError(f"{path}: duplicate card id {card.id!r}")
        cards[card.id] = card
    return cards
