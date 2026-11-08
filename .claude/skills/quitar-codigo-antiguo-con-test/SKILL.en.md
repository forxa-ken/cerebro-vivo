---
name: quitar-codigo-antiguo-con-test
description: Use when removing an old function, window or feature.
---

# Remove old code with a test

## How (steps)
1. Search for every reference (`Grep`) before deleting: functions, `window.x = x`, tests and texts.
2. Delete only what nobody calls; note what is left unused for a future cleanup.
3. Change the test that demanded its existence into one that demands its absence (`assertNotIn`).
4. Run the full suite and ask Darwin to test the affected buttons.

## Error it prevents (real case)
- The old windows of the dev panel stayed as a fallback until Darwin said so.

## Where it lives in the repo
- `static/js/app.js`, `tests/test_admin_page.py`

## Source
- #68, item 000b, spec 028

## Used
- Times: 0 · Last: — (created on 2026-10-31, spec 079)
