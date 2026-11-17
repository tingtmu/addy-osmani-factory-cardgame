from pathlib import Path

from cardengine.loader import load_cards


def test_load_one_card_fixture() -> None:
    cards = load_cards(Path(__file__).parent / "fixtures" / "one_card.json")

    assert set(cards) == {"strike"}
    card = cards["strike"]
    assert card.id == "strike"
    assert card.name == "Strike"
    assert card.cost == 1
    assert len(card.effects) == 1
    effect = card.effects[0]
    assert effect.type == "damage"
    assert dict(effect.params) == {"amount": 6}
