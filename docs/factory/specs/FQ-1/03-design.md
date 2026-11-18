# FQ-1 / Gate 3 - Program design

## Files
New:
- `pyproject.toml` - package `cardengine`, pytest/ruff/mypy config (mypy uses `exclude`
  for .venv, docs, .claude, .agents, .codex so `mypy .` only checks src and tests)
- `.gitignore` - `.venv`, `__pycache__`, tool caches
- `src/cardengine/__init__.py`
- `src/cardengine/models.py` - `Effect`, `Card`, `Status`, `Unit`
- `src/cardengine/effects.py` - effect-type registry and per-type validation
- `src/cardengine/loader.py` - `load_cards`, `parse_card`, `CardDataError`
- `data/cards.json` (created only in slice 5)
- `tests/fixtures/one_card.json`
- `tests/test_smoke.py`, `tests/test_loader.py`, `tests/test_effects.py`,
  `tests/test_loader_errors.py`, `tests/test_models.py`, `tests/test_starter_cards.py`
Modified: none. Every test file is created once and never edited by a later slice.

## Contracts (no implementations)
```python
# models.py
@dataclass(frozen=True) class Effect: type: str; params: Mapping[str, int | str]
@dataclass(frozen=True) class Card: id: str; name: str; cost: int; effects: tuple[Effect, ...]
@dataclass(frozen=True) class Status: name: str; stacks: int; duration: int | None
@dataclass class Unit: name: str; max_hp: int; hp: int; energy: int;
                      deck: list[Card]; hand: list[Card]; discard: list[Card]

# effects.py
EFFECT_TYPES: Mapping[str, EffectSpec]       # type name -> required/optional fields
def parse_effect(raw: Mapping[str, object], card_id: str) -> Effect

# loader.py
class CardDataError(ValueError): ...
def parse_card(raw: Mapping[str, object]) -> Card
def load_cards(path: Path) -> dict[str, Card]
```

## Call stack (main flow)
`load_cards` -> `json.load` -> for each entry `parse_card` -> `parse_effect` x N ->
`EFFECT_TYPES[type]` validation -> `Card` -> dict keyed by id (duplicate check).

## Tests (what each proves)
- test_smoke: package imports (proves tooling and gates work).
- test_models: Card/Effect cannot be reassigned (frozen, shallow: attributes cannot be reassigned, params contents are not copied or wrapped);
  Status duration None means permanent; Unit holds zones independently.
- test_effects: each of 4 types accepts valid params; rejects unknown type, missing field,
  unknown extra field, non-positive amount, wrong value type, and bool-as-int.
- test_loader: one-card fixture loads into the expected Card.
- test_loader_errors: duplicate id, negative cost, empty effects, missing name raise
  `CardDataError` containing the card id; malformed JSON raises it naming the file path.
- test_starter_cards: exactly Strike/Defend/Quick Study load with expected effects, and a
  4th card in a temp JSON file loads with no code change (the data-only constraint).

## Three decisions I am least confident about
1. Effect as generic `type + params mapping` vs one dataclass per effect type. Generic keeps
   "new card = data only" cheap but gives weaker static typing; revisit if Milestone 2
   interpreters get messy.
2. `apply_status` is validated now although no starter card uses it, to avoid reshaping the
   schema in Milestone 3. Risk: guessing fields (`stacks`, `duration`) before behavior exists.
3. `Unit` and `Status` shapes are included in Milestone 1 per spec.md ("data structures")
   with no behavior; they may need field changes once turn flow exists.
