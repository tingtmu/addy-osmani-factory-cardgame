# FQ-1 / Gate 2 - Architecture

## Systems touched
Greenfield: no existing modules. New Python package `cardengine` under `src/`, a `data/`
directory for card definitions, and `tests/`. No existing code is modified.

## Data structures (shapes)
- `Effect`: `{ "type": "damage" | "shield" | "draw" | "apply_status", ... }`
  - `damage` / `shield` / `draw`: integer `amount` > 0
  - `apply_status`: `status` (string name), `stacks` > 0, optional `duration` > 0
- `Card`: `id` (unique string), `name`, `cost` (int >= 0), `effects` (non-empty list)
- `Status`: `name`, `stacks`, `duration` (shape only; behavior is Milestone 3)
- `Unit`: `name`, `max_hp`, `hp`, `energy`, `deck`/`hand`/`discard` (lists of Card)
  (shape only; behavior is Milestone 2)

Cards live in `data/cards.json` as `{ "cards": [ ... ] }`.

## Call flow (end to end)
1. `load_cards(path)` reads JSON.
2. Each entry is parsed into `Card` through `parse_card`, which dispatches each effect to
   a registry keyed by effect `type` (adding an effect type later is one registry entry,
   adding a card is data only).
3. Any invalid entry raises `CardDataError` naming the card id and field.
4. Returns a dict of `id -> Card`; duplicate ids are an error.

## External dependencies
None at runtime (stdlib `json`, `dataclasses` only). Dev only: pytest, ruff, mypy.
These are required by `gates.sh`, which finds them on PATH.

## Load-bearing paths
None touched. `.github/workflows`, `.claude/`, `.factory/` are untouched.
Gate level: `full`.

## What could break elsewhere
Nothing exists yet. Risks are forward-looking: effect shape choices constrain
Milestones 2-4, so the registry-by-type design is chosen to keep them additive.
Operational risk: `gates.sh` needs ruff/mypy/pytest on PATH, otherwise the verdict is
MISCONFIGURED; and `mypy .` scans the whole repo, so config uses `exclude` (not `files`,
which an explicit `.` overrides) to skip .venv, docs, .claude, .agents, .codex. Slice 0
sets this up. Gates are invoked as `PATH=.venv/bin:$PATH ./.claude/scripts/gates.sh full`.
