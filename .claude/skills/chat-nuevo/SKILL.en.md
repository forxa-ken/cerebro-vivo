---
name: chat-nuevo
description: Use when Darwin types /chat-nuevo (si, no or estado) or asks to turn on or off that the AI opens the new chat by itself when the chat gets long.
---

# /chat-nuevo — open the new chat by itself, yes or no

Turns on, turns off or shows the `chat_nuevo_auto` setting in `.brain/guardianes/guardianes.json`. It is on by default: when the long-chat notice appears, the AI writes the handoff and opens the new chat itself.

## How (steps)
1. Read the word after the command: `si` (turn on), `no` (turn off) or `estado` (just look). With no word, `estado`.
2. Run `python .brain/guardianes/longitud.py --chat-nuevo WORD`.
3. Tell Darwin in one line how it stands, using the text the script prints. Touch nothing else.

## Error it prevents (real case)
- In Guild Control Forever #14 and #15 the long-chat notice arrived and the AI did not open the new chat: it gave the sentence to paste, and in #15 it said the app refused it without having tried. The rule lived only in cerebro-vivo's memory.

## Where it lives in the repo
- `.claude/skills/chat-nuevo`, `.brain/guardianes/longitud.py` (`chat_nuevo`), `guardianes.json` (`chat_nuevo_auto`), spec 025.

## Source
- Spec 025 (Darwin's request, 2026-11-07)

## Used
- Times: 0 · Last: — (created on 2026-11-07)
