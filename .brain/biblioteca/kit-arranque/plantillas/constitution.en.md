# Constitution of {{NOMBRE}} (non-negotiable rules)

> If a task requires breaking any of these rules, **stop and ask {{DUENO}} for explicit authorization**. Single source of rules for every AI in the project.

1. **Language and tone:** answer in **{{IDIOMA}}**, technical and concise.
2. **Strict scope:** work only on what concerns the requested change; refactoring or rewriting anything else is forbidden.
3. **Tests always green:** `{{PRUEBAS}}` after every change. With everything green and no verified failure, existing code is not altered without a direct order.
4. **Living memory:** when closing each task, one line in `decisions.log` (`python .brain/guardianes/cerrar.py --chat "{{NOMBRE}} #N" "what was done"`) and, if an important decision was made, its `D-NNN` card with the reason why.
5. **Pending list holds only what is missing:** "implemented" is not "finished"; it stays in `pendientes.md` until {{DUENO}} tests it. As soon as they confirm, in that same reply: the detail goes to `archive/hechos.md`, a row to `archive/hechos-indice.md`, and the item leaves `pendientes.md`. Numbering is fixed.
6. **Test memory:** a test campaign with findings opens its `P-NNN` in `.brain/pruebas/`; when a finding is fixed it is ticked `- [x]`.
7. **Secrets:** keys and tokens live in environment variables or in Git-ignored files, never in the repository.
8. **Every external call** has a maximum time and a local plan B.
9. **Push to GitHub** only on {{DUENO}}'s express order. Only exception: `traspaso-out salgo` pushes its memory commit without further order, and asks first if other commits are pending.
10. **The goal is written down:** any goal or change of goal that {{DUENO}} gives in a chat is noted in `.brain/architecture/objetivo.md` in that same reply; what exists only in the chat is lost.
11. **Edit code without terminal tricks:** code blocks (more than 3 lines) are written with the Edit or Write tools, never with a Python script in a heredoc, where `\n` and quotes get mangled; if a script edit is unavoidable, check the syntax (`python -c "import ast; ast.parse(open('FILE', encoding='utf-8').read())"`) before going on.
