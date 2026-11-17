# FQ-1 / Gate 4 - Slices

Each slice is one PR, estimated well under 400 changed lines, `gate_level: full`,
`load_bearing: false`, at most 5 files. Gates are run as
`PATH=.venv/bin:$PATH ./.claude/scripts/gates.sh full` (tools live in `.venv`, created
with `uv venv .venv && uv pip install --python .venv/bin/python pytest ruff mypy`).
Dependencies are stated per slice. No slice edits an existing test file; later slices add
new test files.

## Slice 0 - Tooling skeleton
done_when: gates `full` ends `status=GREEN` with no skips on a package that only imports
(`import cardengine`), proven by one smoke test.
files_expected: pyproject.toml, .gitignore, src/cardengine/__init__.py,
tests/test_smoke.py
Estimate: ~60 lines. Depends on: nothing.

## Slice 1 - Tracer bullet: load one card end to end
done_when: `load_cards(path)` loads a one-card JSON fixture (damage 6) into a `Card`; test
asserts id, name, cost, and the damage effect. Mostly minimal, no validation yet.
files_expected: src/cardengine/models.py, src/cardengine/loader.py,
tests/fixtures/one_card.json, tests/test_loader.py
Estimate: ~120 lines. Depends on: slice 0.

## Slice 2 - Effect registry and validation
done_when: all four effect types validate through `parse_effect`; unknown type, missing
field, unknown extra field, non-positive amount, wrong type, and boolean-instead-of-int
each raise `CardDataError` naming the card id.
files_expected: src/cardengine/effects.py, src/cardengine/loader.py,
tests/test_effects.py
Estimate: ~180 lines. Depends on: slice 1.

## Slice 3 - Card-level validation
done_when: negative cost, empty effects, missing name, duplicate ids are rejected with
`CardDataError` naming the card id; malformed JSON is rejected with an error naming the
file path.
files_expected: src/cardengine/loader.py, tests/test_loader_errors.py
Estimate: ~120 lines. Depends on: slice 2.

## Slice 4 - Status and Unit shapes
done_when: `Status` and `Unit` exist and type-check; tests cover Status construction
(including `duration=None` meaning permanent), Unit zones being independent lists, and
`Card`/`Effect` being immutable.
files_expected: src/cardengine/models.py, tests/test_models.py
Estimate: ~100 lines. Depends on: slice 1 (independent of 2-3).

## Slice 5 - Three starter cards
done_when: `data/cards.json` holds exactly Strike (cost 1, damage 6), Defend (cost 1,
shield 5), Quick Study (cost 1, draw 2); a test copies it to a temp file, appends a 4th
card, and loads it with no engine change.
files_expected: data/cards.json, tests/test_starter_cards.py
Estimate: ~80 lines. Depends on: slices 2-3.

Out of scope for FQ-1, recorded so it is not lost: the seeded random source and shuffling
are specified by spec.md but belong to Milestone 2 (turn flow); a Milestone 2 spec must
include it.
