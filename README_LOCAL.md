# Local Setup and Recovery · 0.4.0

## Play the hosted game

Open https://seiya058904.github.io/epic-battle-sandbox-cn/ . It loads the actual WebGL game, with the sandbox enabled by default. Add `?sandbox=0` to use its separate standard save.

The hosted game downloads its runtime from GitHub Pages and simulates battles locally. It does not require a game account. This is not a promised offline-cached PWA.

## Run a fresh clone

Python 3 and a modern WebGL-capable browser are enough for the packaged build:

~~~powershell
python tools/build_site.py
python -m http.server 8766 --bind 127.0.0.1 --directory output/pages
~~~

Open **http://127.0.0.1:8766/**. Stop the server with Ctrl+C. The packager validates the five reviewed runtime files in `web-build/` against `evidence/public-assets.json`. It does not download or modify assets.

## Preserve an existing personal installation

The original local installation still runs with:

~~~powershell
./Start-Local.ps1
~~~

It uses **http://127.0.0.1:8765/local.html** and `../player-profile`. Do not change that port, replace 127.0.0.1 with localhost, or use file:// if you want to keep using that exact save location. The original six files remain in `Build/`, `TemplateData/` and `index.html`, with a separate copy in `../original-backup/`.

## Save isolation

| Entry | Standard database | Sandbox database |
| --- | --- | --- |
| Original local launcher, port 8765 | `/idbfs` | `/idbfs-ebs-local-sandbox-v2` |
| GitHub Pages | `/idbfs-ebs-pages-standard-v1` | `/idbfs-ebs-pages-sandbox-v1` |
| Packaged local preview, port 8766 | Same names as hosted, on its own origin | Same names as hosted, on its own origin |

The original local initialization can copy a valid old v1 sandbox or standard save. Hosted initialization only considers its own project-specific standard database. It never imports the shared origin's unrelated `/idbfs` or local legacy database names.

Unity also derives the internal persistent directory from the page URL. The supported Pages path and both localhost origins have separately verified directory hashes. Keep these URLs stable; moving the game to another domain or project path requires updating and testing that mapping.

Separate names prevent accidental save mixing. They are not a security boundary between untrusted sites on the same web origin.

## Sandbox behavior

- Gems are set to `999999999` before each sandbox launch. Spending is real, and the upstream build may add its own starting bonus. This is a finite balance.
- All 37 troop types are set to Level 3, including the eight epic types' separate level keys.
- Local epic availability and level progress are set in the isolated sandbox state. Purchase receipts, subscription flags and online account permissions are not changed.
- Level coins are `999999999`; army and per-type quotas are `1000`. Terrain, collisions, team areas and hardware limits remain.
- The automatic ad countdown component is disabled. Rating prompts and some untranslated artwork remain.
- Browser storage can still be removed by browser settings or storage eviction. There is no cloud-save service.

## Rebuild the asset patches

This is optional when playing the packaged runtime. For controlled analysis, supply the exact original files you have permission to use; the import script checks all hashes before copying and refuses to overwrite a different file.

~~~powershell
python tools/import_originals.py --from-directory "PATH-TO-ORIGINAL-BUILD"
python tools/verify_originals.py
python -m venv ../analysis-env
../analysis-env/Scripts/python.exe -m pip install -r tools/requirements-analysis.txt
~~~

Download [Noto Sans CJK SC Regular](https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf) to `../tool-cache/NotoSansCJKsc-Regular.otf`. Its required SHA-256 is `2c76254f6fc379fddfce0a7e84fb5385bb135d3e399294f6eeb6680d0365b74b`. See [the OFL license](localization/OFL-Noto.txt).

~~~powershell
../analysis-env/Scripts/python.exe tools/build_local.py
../analysis-env/Scripts/python.exe tools/build_sandbox.py
../analysis-env/Scripts/python.exe tools/build_native_ui.py
~~~

The final runtime uses `EBS.zh-CN.ui.data`, `EBS.sandbox.ui.data` and `EBS.local.framework.js`, plus the original loader and WASM. Generated files remain under `local-generated/`; a new public runtime must be reviewed and its exact hashes added to the asset manifest before publication. Do not blindly replace binary strings or originals.

## Verification

~~~powershell
python tools/check_public.py
python -m unittest discover -s tools -p test_public.py -v
node tools/test_prefs.cjs
python tools/test_hosted_storage.py
python tools/qa_playable_site.py http://127.0.0.1:8766/
python tools/qa_playable_site.py http://127.0.0.1:8766/ --mobile
~~~

Browser tests use Python Playwright and an existing Chromium executable; set `EBS_CHROMIUM` if needed. The Browser plugin was unavailable during verification. Tests use temporary or dedicated QA contexts, never the personal player profile. Inspect screenshots before claiming a visual pass.

With original assets and the port-8765 server available, `python tools/verify_originals.py` and `python tools/test_storage.py` also verify unchanged originals and legacy local-save behavior.

## Recovery

1. Return to a menu before switching modes. Add `?sandbox=0` to the same game URL for standard mode. This does not delete the sandbox database.
2. Existing personal installations can open `http://127.0.0.1:8765/index.html` for the byte-identical original build. That original entry may attempt external services; use request interception for a strict offline comparison.
3. Run `python tools/verify_originals.py` before restoring originals. Preserve a differing file separately rather than overwriting it.
4. Use `git revert <commit>` to undo source changes. Do not run blanket cleanup: untracked files include local originals and saves.
5. The old pre-public history exists only on the original workstation in `../local-archive/pre-public-history.bundle`. To recover it into a separate directory:

~~~powershell
git bundle verify ../local-archive/pre-public-history.bundle
git clone --branch local/zh-buttons-noads ../local-archive/pre-public-history.bundle ../history-recovery
~~~

Old commits: 0.1.0 `60192d9`, 0.2.0 `669bbe4`, 0.3.0 `793eb31`, 0.3.1 `62a452e`. They do not exist in the fresh public history. Never restore an old .git directory over the current repository, or overwrite `player-profile`.

The earlier documentation-only website is preserved in public commit `3f88cd5`. Reverting to it restores a project guide, not a playable deployment.

## What stays local

Personal browser profiles, old history bundles, original backups, extraction output and QA scratch files stay outside the public payload. The earlier cleanup receipt is stored in `../local-archive/cleanup-receipt.json`; removed items went to the Windows Recycle Bin. Original assets and the personal save were retained.

The public runtime is an explicitly approved subset under `web-build/`, with real README screenshots under `docs/media/`. These are the only binary publication exceptions.

## Synchronization

~~~powershell
git status --short
python tools/check_public.py
git fetch origin
git rev-list --left-right --count HEAD...origin/main
~~~

A result of `0 0` means local HEAD and origin/main match. Also verify the workflow's head SHA, deployment result and live runtime hashes; a local test alone is not deployment proof.
