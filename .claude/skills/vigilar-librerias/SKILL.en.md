---
name: vigilar-librerias
description: Use when adding, updating or auditing a Python library.
---

# Watch libraries

## How (steps)
1. Run `librerias.py` by hand every 7 days (it queries OSV.dev and PyPI with a timeout).
2. Startup only reads the result and warns if it is 10 days old or more.
3. It only warns: it never updates or installs by itself; false alarms go to the `ignorar` list with a reason.
4. Detail in `architecture/librerias.md`.

## Error it prevents (real case)
- `requirements.txt` does not pin versions and nobody was checking known security flaws.

## Where it lives in the repo
- `.brain/guardianes/librerias.py`, `.brain/architecture/librerias.md`

## Source
- D-047

## Used
- Times: 0 · Last: — (created on 2026-10-31, spec 079)
