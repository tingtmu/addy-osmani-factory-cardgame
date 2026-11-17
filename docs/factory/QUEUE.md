# Factory queue snapshot

The operational queue lives in GitHub issue labels. This file is a reviewable snapshot
written by `factory-triage` and reported by `/factory`; implementation routines query
GitHub directly.

An unmerged update to this file must never block a later routine from seeing work. Durable
run evidence lives in one file per run under `docs/factory/runs/`.

**Dispositions**

| Disposition | Next stage |
|---|---|
| `ready-to-implement` | factory-implement picks it up |
| `ready-to-spec` | human runs factory-spec |
| `needs-info` | parked, question is on the issue |
| `wait-to-implement` | parked, blocker named below |
| `awaiting-review` | PR open, human owns it |
| `done` | merged by a human |

The corresponding live labels use the `factory:` prefix, for example
`factory:ready-to-implement` and `factory:awaiting-review`. The live issue also carries a
`factory-handoff:v1` comment with the fields needed by implementation.

---

## FQ-1 (Milestone 1: data structures and 3 starter cards), from docs/factory/specs/FQ-1/
All entries: load_bearing false, gate_level full, confidence high, last_triaged 2026-11-17.

- #2 slice 0 Tooling skeleton: ready-to-implement. files: pyproject.toml, .gitignore, src/cardengine/__init__.py, tests/test_smoke.py. done_when: gates full GREEN with no skips; smoke test imports cardengine.
- #3 slice 1 Tracer bullet: wait-to-implement (slice 0). files: models.py, loader.py, tests/fixtures/one_card.json, tests/test_loader.py.
- #4 slice 2 Effect registry and validation: wait-to-implement (slice 1). files: effects.py, loader.py, tests/test_effects.py.
- #5 slice 3 Card-level validation: wait-to-implement (slice 2). files: loader.py, tests/test_loader_errors.py.
- #6 slice 4 Status and Unit shapes: wait-to-implement (slice 1). files: models.py, tests/test_models.py.
- #7 slice 5 Three starter cards: wait-to-implement (slices 2, 3). files: data/cards.json, tests/test_starter_cards.py.

---
