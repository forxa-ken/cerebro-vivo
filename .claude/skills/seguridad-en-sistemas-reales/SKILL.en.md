---
name: seguridad-en-sistemas-reales
description: Use when the project will act on real servers, infrastructure or data (VMware, nube, bases de datos) or when writing the motor/reglas de seguridad of such a project.
---

# Safety on real systems

Rules that, in the VMware experiment (rounds 3 and 4, 2026-11-09), separated safe code from unsafe code. Without them, both Cerebro Vivo and ODD left an engine that depended on internal details of the lab. With them, both came out equally safe.

## How (steps)
1. **Every change goes through the engine.** The command line and the modules never call the server directly to change something.
2. **When in doubt, ask for approval (fail towards safe).** If it cannot be known whether an action is delicate (machine state, size, whether a piece of data exists), treat it as delicate.
3. **Safety rules do not depend on internal details of the lab.** Query the server only through methods of its interface; a real one will not have the simulator's internal attributes.
4. **Every safety rule has a test with a minimal fake server** (only `describir` and `ejecutar`, no internal attributes) proving it still demands approval.
5. **Odd inputs** (empty names, zero, negative, text or missing sizes, repeated names) are rejected with a clear, logged error before touching anything.
6. **Checklist before closing**, written in the result: which actions are delicate, what happens if information is missing, what happens with odd inputs, what was logged, that there are no credentials. If a point fails, fix it before closing.
7. **Safety without changing what was asked.** No AI changes or removes a requirement "for security". If it sees a risk, it records it as a gap or proposal and asks Darwin (in an AI factory, spec 035, rule R9).

## Error it prevents (real case)
- Round 3: one branch's engine asked the server `es_en_caliente` and, if it did not exist, **acted without approval** on a running machine. Its 29 tests missed it because they only used the lab.
- Round 4: two branches without these rules crashed with an internal error against a different server: they did not act, but by accident and leaving no record.

## Where it lives in the repo
- `.brain/archive/informe-experimento-vmware-ronda3-2026-11-09.md` and `...ronda4-2026-11-09.md` (tests and results).

## Source
- Cerebro Vivo vs ODD experiment, pending item 37 (sample of 1 per cell: a trend, not proof).

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not logged here) (created on 2026-11-09)
