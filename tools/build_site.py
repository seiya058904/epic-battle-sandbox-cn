"""Assemble the authorized playable site from an exact, hash-checked file list."""
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/pages'


def main():
    manifest = json.loads((ROOT / 'evidence/public-assets.json').read_text(encoding='utf-8'))
    files = {path.name: path for path in (ROOT / 'site').iterdir() if path.is_file()}
    files.update({name: ROOT / name for name in ('local-mode.js', 'prefs-codec.js')})
    files['licenses/OFL-Noto.txt'] = ROOT / 'localization/OFL-Noto.txt'
    files['NOTICE.txt'] = ROOT / 'NOTICE.md'
    for row in manifest['files']:
        if not row['path'].startswith('web-build/'):
            continue
        path = ROOT / row['path']
        if hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']:
            raise SystemExit(f'Runtime hash mismatch: {path.name}')
        files['Build/' + path.name] = path
    # Reject stale output instead of deleting an uncertain directory.
    existing = {p.relative_to(OUT).as_posix() for p in OUT.rglob('*') if p.is_file()}
    if existing - files.keys():
        raise SystemExit(f'Unexpected old output files; review before recycling: {sorted(existing-files.keys())}')
    for name, source in files.items():
        target = OUT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    if sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file()) >= 1_000_000_000:
        raise SystemExit('Pages site exceeds the 1 GB limit')
    print(f'PASS: playable Pages site assembled with {len(files)} files in {OUT}')


if __name__ == '__main__':
    main()
