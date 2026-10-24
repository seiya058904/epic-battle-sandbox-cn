# Project rules

- Public repository: patch code, text evidence, documentation and `site/` only.
- Never stage game assets, generated builds, extracted resources, screenshots of the game, browser profiles, local backups or old Git bundles. Run `python tools/check_public.py` before pushing.
- Deploy only `site/`. The GitHub Pages site is documentation, not a playable game.
- Preserve the fixed local origin `http://127.0.0.1:8765` and the user's `../player-profile`.
- Preserve original bytes and separate backups. Game behavior changes require real consumption/UI verification; no HUD-only success claims.
- Keep PARTIAL and NOT TESTED distinct from PASS. Existing evidence describes the recorded build, not future changes.
- No subagents. No public mutations beyond the user's requested scope.
