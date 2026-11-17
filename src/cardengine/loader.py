import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any, cast

from cardengine.effects import CardDataError, parse_effect
from cardengine.models import Card

__all__ = ["CardDataError", "load_cards", "parse_card"]


def parse_card(raw: Mapping[str, object]) -> Card:
    card_id = str(raw.get("id"))
    raw_effects = cast(list[Mapping[str, object]], raw["effects"])
    return Card(
        id=cast(str, raw["id"]),
        name=cast(str, raw["name"]),
        cost=cast(int, raw["cost"]),
        effects=tuple(parse_effect(effect, card_id) for effect in raw_effects),
    )


def load_cards(path: Path) -> dict[str, Card]:
    with path.open(encoding="utf-8") as handle:
        data = cast(dict[str, Any], json.load(handle))
    raw_cards = cast(list[dict[str, Any]], data["cards"])
    cards = [parse_card(raw) for raw in raw_cards]
    return {card.id: card for card in cards}
