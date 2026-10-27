![Illustrated opposing formations on a green battlefield](docs/media/readme-cover.svg)

# Epic Battle Sandbox CN

An unofficial single-player modification of a compiled Unity WebGL battle game, with a partially localized Simplified Chinese interface, max-level troops, and expanded sandbox resources.

[Play online](https://seiya058904.github.io/epic-battle-sandbox-cn/) · [Run locally](#run-locally) · [Actual formation screenshot](docs/media/formation.png)

*Original battlefield illustration, not game footage or official upstream artwork.*

## Features

- **Arrange a matchup:** select troops, place both sides within the deployment areas, and watch the existing 3D combat simulation.
- **Use the sandbox roster:** the local sandbox state sets all 37 troop types to Level 3 and makes eight epic troop types available there.
- **Experiment with expanded limits:** sandbox resources and deployment budgets are large finite values; terrain, collision, and placement rules still apply.
- **Read a partially Chinese interface:** common menu, deployment, pause, and result labels are translated inside the Unity canvas. Some artwork, prompts, and branding remain in their original language.
- **Keep modes separate:** sandbox and standard mode use separate browser databases, with project-specific hosted save names.

[View the actual deployment screen](docs/media/formation.png) or the [troop upgrade screen](docs/media/upgrades.png). These are preserved gameplay captures from the reviewed publication set, not concept art.

## How to play

1. Open Custom Battle for a free-form matchup, or choose a regular or epic level.
2. Select troops and click or tap a valid position to place them.
3. Use the battle button to start; pause and resume through the in-game controls.
4. Return to setup and adjust the formation to try another matchup.

The sandbox seeds a large gem balance and raises deployment quotas; those values are not infinite and are not a performance guarantee. The automatic advertising countdown is disabled, although the original rating prompt may still appear. The game is single-player and does not alter online accounts, purchases, subscriptions, or leaderboards.

## Run locally

**Prerequisites:** Python 3 and a modern WebGL-capable browser. From the repository root:

```sh
python tools/build_site.py
python -m http.server 8766 --bind 127.0.0.1 --directory output/pages
```

Open `http://127.0.0.1:8766/`. The first load downloads the packaged runtime; the hosted edition needs a connection to fetch its files, and complete offline caching is not promised. Saves belong to the current browser and origin and do not automatically transfer between Pages and localhost.

The prepared runtime lives in [`web-build/`](web-build/). Rebuilding the underlying patches is a separate workflow; see [local setup and recovery](README_LOCAL.md). An existing personal installation can continue using `Start-Local.ps1` at its original port, 8765, without changing its profile. Add `?sandbox=0` to the game URL for standard mode.

## Verification and limits

```sh
python tools/check_public.py
python -m unittest discover -s tools -p test_public.py -v
node tools/test_prefs.cjs
```

The [audit](AUDIT.md) and [evidence](evidence/) distinguish actual checks from untested areas. Historical Chromium checks exercised deployment, combat, pause, resume, results, and reopening; they do not certify every level, device, or a 1,000-unit battle. Landscape orientation is recommended on phones, and physical Android validation remains pending.

The publication boundary permits only reviewed runtime and screenshot bytes identified in [`evidence/public-assets.json`](evidence/public-assets.json); personal profiles, extracted resources, and old backups are excluded.

## Repository map

- [`site/`](site/) — game page and loading interface.
- [`web-build/`](web-build/) — hash-locked compiled WebGL runtime.
- [`localization/`](localization/) — translation tables and font license.
- [`tools/`](tools/) and [`evidence/`](evidence/) — packaging, verification, and recorded evidence.
- [`local-mode.js`](local-mode.js) and [`prefs-codec.js`](prefs-codec.js) — local and hosted save initialization.

## Provenance and rights

The analyzed build came from [CoreScripts/epicbattlesimulator2](https://github.com/CoreScripts/epicbattlesimulator2), pinned to commit `5b6e7f7`. It is compiled WebGL material, not an editable Unity source project; its title does not establish that it is the authorized Rappid Studios mobile release.

The maintainer's permission to publish this modification and its required runtime assets is recorded in [NOTICE.md](NOTICE.md); it is not an independently verified license for further redistribution. Game code, models, textures, audio, and branding remain subject to their owners' rights. Noto font usage follows the included [OFL terms](localization/OFL-Noto.txt). This project is not affiliated with or endorsed by the original developers.
