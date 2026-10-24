# Provenance, Permission and Publication Scope

The maintainer explicitly confirmed on 2026-10-24 that their authorization permits public deployment of this modified WebGL game and distribution of its required program and visual assets. Publication is based on that confirmation; this repository does not claim to independently verify a separate license document or provide official endorsement.

The permitted publication set is recorded by exact file size and SHA-256 in `evidence/public-assets.json`: the original loader and WASM, the reviewed modified framework, two reviewed UI/data variants, and selected actual gameplay screenshots. Personal saves, profiles, old Git bundles and extracted analysis resources are not published.

## Original game

The analyzed build came from [CoreScripts/epicbattlesimulator2](https://github.com/CoreScripts/epicbattlesimulator2), pinned to `5b6e7f7035a4246fac6f58aca6799d5eaacfcc5d`. It contains compiled WebGL artifacts, not an editable Unity source project.

Its configuration references madkidgames.com and H5_OnDomainApproved. The repository title does not establish that this is the authorized Rappid Studios mobile release. The project is an unofficial modification and does not claim affiliation with the original developers.

Game code, models, textures, audio, branding and other third-party materials remain subject to their respective owners' rights. Public availability here is not an open-source license or a grant for further redistribution.

## Fonts and modification code

Chinese glyphs use Noto CJK under the SIL Open Font License. The license is included at `localization/OFL-Noto.txt`. The complete upstream font file is not separately distributed in this repository; the game data contains the generated glyph atlas.

No general open-source license has been declared for the modification code. Do not infer a license for third-party assets from source visibility.

## Single-player boundary

The sandbox changes browser-local progression and resources only. It does not alter online accounts, leaderboards, server balances, payment receipts or subscription flags. Local epic-unit availability is not proof of a real purchase. Runtime external service requests are constrained by the page's same-origin content security policy.

Historical evidence refers to local screenshot files; the public `docs/media/` images are a selected presentation set. Audit claims distinguish actual tests from untested areas.
