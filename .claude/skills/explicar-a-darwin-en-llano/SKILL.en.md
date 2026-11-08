---
name: explicar-a-darwin-en-llano
description: Use when explaining something technical to Darwin, the project owner.
---

# Explain to Darwin in plain language

## How (steps)
1. Answer in the project's language, without jargon: say what it does, not how it is programmed.
2. Give concrete steps to test (what to press, what to look for).
3. Name which test is missing and what it consists of.
4. Warn when the chat gets long and recommend opening a new chat (`NAME #N`).

## Error it prevents (real case)
- Darwin is not a programmer and learns with the project; jargon blocks him.

## Where it lives in the repo
- `CLAUDE.md`, the assistant's memory

## Source
- memory "Darwin is not a programmer"

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not logged here) (created on 2026-10-31, spec 079)
