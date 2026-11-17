from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal

from cardengine.models import Effect

FieldKind = Literal["positive_int", "non_empty_str"]


class CardDataError(ValueError):
    """Raised when card data does not match the expected schema."""


@dataclass(frozen=True)
class EffectSpec:
    required: Mapping[str, FieldKind]
    optional: Mapping[str, FieldKind]


# Adding an effect type is one entry here. Keys are the `type` values found in card data.
EFFECT_TYPES: Mapping[str, EffectSpec] = {
    "damage": EffectSpec(required={"amount": "positive_int"}, optional={}),
    "shield": EffectSpec(required={"amount": "positive_int"}, optional={}),
    "draw": EffectSpec(required={"amount": "positive_int"}, optional={}),
    "apply_status": EffectSpec(
        required={"status": "non_empty_str", "stacks": "positive_int"},
        optional={"duration": "positive_int"},
    ),
}


def _check_field(
    card_id: str, effect_type: str, name: str, kind: FieldKind, value: object
) -> int | str:
    where = f"card {card_id}: effect {effect_type!r} field {name!r}"
    if kind == "positive_int":
        # bool is a subclass of int in Python, so it must be excluded explicitly.
        if isinstance(value, bool) or not isinstance(value, int):
            raise CardDataError(f"{where} must be an integer, got {value!r}")
        if value <= 0:
            raise CardDataError(f"{where} must be greater than 0, got {value}")
        return value
    if not isinstance(value, str) or not value.strip():
        raise CardDataError(f"{where} must be a non-empty string, got {value!r}")
    return value


def parse_effect(raw: Mapping[str, object], card_id: str) -> Effect:
    if "type" not in raw:
        raise CardDataError(f"card {card_id}: effect is missing required field 'type'")
    effect_type = raw["type"]
    if not isinstance(effect_type, str):
        raise CardDataError(f"card {card_id}: effect 'type' must be a string, got {effect_type!r}")
    spec = EFFECT_TYPES.get(effect_type)
    if spec is None:
        raise CardDataError(f"card {card_id}: unknown effect type {effect_type!r}")

    for name in spec.required:
        if name not in raw:
            raise CardDataError(
                f"card {card_id}: effect {effect_type!r} is missing required field {name!r}"
            )

    allowed = set(spec.required) | set(spec.optional)
    for name in raw:
        if name == "type":
            continue
        if name not in allowed:
            raise CardDataError(
                f"card {card_id}: effect {effect_type!r} has unknown field {name!r}"
            )

    params: dict[str, int | str] = {}
    for name, kind in {**spec.required, **spec.optional}.items():
        if name not in raw:
            continue
        params[name] = _check_field(card_id, effect_type, name, kind, raw[name])
    return Effect(type=effect_type, params=params)
