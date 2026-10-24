"""Import six user-supplied originals without replacing any differing file."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--from-directory', required=True, type=Path)
    source = parser.parse_args().from_directory.resolve()
    rows = json.loads((ROOT / 'evidence/baseline-manifest.json').read_text())['files']
    targets = (ROOT, ROOT.parent / 'original-backup')
    # Validate the complete plan before copying any bytes.
    for row in rows:
        path = source / row['path']
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']:
            raise SystemExit(f'Wrong or missing original: {path}')
        for base in targets:
            target = base / row['path']
            if target.exists() and (not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != row['sha256']):
                raise SystemExit(f'Refusing to replace differing file: {target}')
    for row in rows:
        for base in targets:
            target = base / row['path']
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open('xb') as output, (source / row['path']).open('rb') as original:
                    shutil.copyfileobj(original, output)
            if hashlib.sha256(target.read_bytes()).hexdigest() != row['sha256']:
                raise SystemExit(f'Copy verification failed: {target}')
    print('PASS: six originals and six independent backups match the baseline')


if __name__ == '__main__':
    main()
