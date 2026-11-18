import json
import shutil
from pathlib import Path

from cardengine.loader import load_cards

STARTER_PATH = Path(__file__).resolve().parents[1] / "data" / "cards.json"


def test_starter_cards_load_with_expected_ids_costs_and_effects() -> None:
    cards = load_cards(STARTER_PATH)

    assert set(cards) == {"strike", "defend", "quick_study"}

    expected = {
        "strike": ("Strike", 1, "damage", 6),
        "defend": ("Defend", 1, "shield", 5),
        "quick_study": ("Quick Study", 1, "draw", 2),
    }
    for card_id, (name, cost, effect_type, amount) in expected.items():
        card = cards[card_id]
        assert card.id == card_id
        assert card.name == name
        assert card.cost == cost
        assert len(card.effects) == 1
        effect = card.effects[0]
        assert effect.type == effect_type
        assert effect.params["amount"] == amount


def test_appending_a_card_to_a_copy_loads_four_and_keeps_originals(tmp_path: Path) -> None:
    copy_path = tmp_path / "cards.json"
    shutil.copyfile(STARTER_PATH, copy_path)

    data = json.loads(copy_path.read_text(encoding="utf-8"))
    new_card = {
        "id": "heavy_blow",
        "name": "Heavy Blow",
        "cost": 2,
        "effects": [{"type": "damage", "amount": 12}],
    }
    data["cards"].append(new_card)
    copy_path.write_text(json.dumps(data), encoding="utf-8")

    original = load_cards(STARTER_PATH)
    extended = load_cards(copy_path)

    assert len(extended) == 4
    assert "heavy_blow" in extended
    for card_id in ("strike", "defend", "quick_study"):
        assert extended[card_id] == original[card_id]
