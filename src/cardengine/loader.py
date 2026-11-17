import json
from pathlib import Path
from typing import Any, cast

from cardengine.models import Card, Effect


def _load_effect(raw: dict[str, Any]) -> Effect:
    params: dict[str, int | str] = {
        key: cast(int | str, value) for key, value in raw.items() if key != "type"
    }
    return Effect(type=cast(str, raw["type"]), params=params)


def _load_card(raw: dict[str, Any]) -> Card:
    raw_effects = cast(list[dict[str, Any]], raw["effects"])
    return Card(
        id=cast(str, raw["id"]),
        name=cast(str, raw["name"]),
        cost=cast(int, raw["cost"]),
        effects=tuple(_load_effect(effect) for effect in raw_effects),
    )


def load_cards(path: Path) -> dict[str, Card]:
    with path.open(encoding="utf-8") as handle:
        data = cast(dict[str, Any], json.load(handle))
    raw_cards = cast(list[dict[str, Any]], data["cards"])
    cards = [_load_card(raw) for raw in raw_cards]
    return {card.id: card for card in cards}
