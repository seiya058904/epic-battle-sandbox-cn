"""Read-only byte verification of working originals and separate backup."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'evidence/baseline-manifest.json').read_text())
for row in manifest['files']:
    for base in (ROOT,ROOT.parent/'original-backup'):
        path=base/row['path']
        assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256'],str(path)
print('PASS: all six original files and all six backups match baseline SHA-256')
