# Project rules

- The user confirmed permission to publicly deploy and distribute the modified WebGL game on 2026-10-24. Publish only the exact runtime files and screenshots listed in `evidence/public-assets.json`, alongside source and documentation.
- Never stage personal browser profiles, extracted analysis resources, local backups or old Git bundles. Run `python tools/check_public.py` before pushing; runtime files and screenshots must match the reviewed SHA-256 allowlist.
- Build the playable Pages site with `python tools/build_site.py`, then deploy only `output/pages/`. Preserve the original single-player gameplay and no extra top toolbar.
- Hosted saves use project-specific database names; never import an unrelated `/idbfs` from another project on the shared GitHub Pages origin.
- Preserve the fixed local origin `http://127.0.0.1:8765` and the user's `../player-profile`.
- Preserve original bytes and separate backups. Game behavior changes require real consumption/UI verification; no HUD-only success claims.
- Keep PARTIAL and NOT TESTED distinct from PASS. Existing evidence describes the recorded build, not future changes.
- No subagents. No public mutations beyond the user's requested scope.
