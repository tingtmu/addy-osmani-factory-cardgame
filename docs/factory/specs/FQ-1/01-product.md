# FQ-1 / Gate 1 - Product: data-driven cards (Milestone 1)

## The person's problem
A designer of a roguelike card game wants to invent new cards ("deal 6 damage", "gain 5
shield", "draw 2 cards") by writing a small data entry, without asking a programmer to
change the game's code each time. Today there is nothing: no way to describe a card.

## What success looks like
- A designer can open one data file, read the three starter cards, and understand them.
- A designer can add a fourth card by editing only that data file; the game accepts it.
- A typo (unknown effect, negative cost) is rejected with a message that names the card
  and the problem, instead of silently doing nothing.
- Measurable: 3 starter cards load; a 4th card added through data alone loads with zero
  engine changes; every invalid-card case in the test list is rejected with a clear error.

- The game's basic building blocks - cards, effects, statuses (poison and the like) and
  units (the player and enemies) - each have a defined shape the later milestones build on.

## Announcement (as if shipped)
> Cards are now data. The starter set - Strike, Defend, Quick Study - lives in a single
> file. Add a card by adding an entry; the engine validates it and tells you exactly what
> is wrong if it is malformed. Combat itself comes in the next milestone.

## Mockups
None. This is a pure-logic engine with no screens.

## What we are deliberately not doing
- No turn flow, hand/draw mechanics, or playing cards (Milestone 2).
- No status effect behavior - poison, weakness, shield decay (Milestone 3). Status is only
  a data shape this milestone.
- No enemy AI (Milestone 4).
- No random numbers or shuffling (arrives with the turn flow, Milestone 2).
- No UI, no save files, no card balance tuning.
