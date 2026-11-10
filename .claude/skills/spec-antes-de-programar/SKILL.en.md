---
name: spec-antes-de-programar
description: Use when a change touches quotas, payments, licenses, deployment, the database, real servers or security rules, or cannot be resumed from the request plus the git diff.
---

# Spec before programming

## How (steps)
0. **Is a spec needed?** Yes if the change touches quotas, payments, licenses, deployment, the database, real servers or security rules. For everything else, **resume test**: if another AI can continue from just the request and the `git diff`, it is a small task and goes straight through the small-change lane, with the security rules, the log and the usual lesson. The number of files no longer decides.
1. Create `.brain/specs/NNN-name.md` from `_template.md`: goal, scope, out of scope, plan, verification. **Write each rule only once** (saying it two ways causes approver rejections).
2. Wait for Darwin's approval before programming.
3. Everything else goes by the small-change lane: direct change, tests green and a line in `decisions.log`.
4. On closing: a D-NNN card if there was an important decision.

## Error it prevents (real case)
- Programming without a plan in big changes produces messy code and repeated work.

## Where it lives in the repo
- `.brain/specs/`, `.brain/specs/_template.md`

## Source
- D-001

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not logged here) (created on 2026-10-31, spec 079)
