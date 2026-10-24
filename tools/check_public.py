"""Fail closed if a tracked file or reachable historical blob is outside public scope."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
TOP = {'.gitignore', '.gitattributes', 'AGENTS.md', 'README.md', 'README_LOCAL.md',
       'AUDIT.md', 'NOTICE.md', 'CHANGELOG.md', 'PRODUCT.md', 'DESIGN.md',
       'Start-Local.ps1', 'local.html', 'local-mode.js', 'prefs-codec.js'}
FOLDERS = {'.github', 'evidence', 'localization', 'tools', 'site'}
TEXT = {'.md', '.py', '.js', '.cjs', '.html', '.css', '.json', '.txt', '.yml', '.svg'}


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def allowed(name):
    p = Path(name)
    return name in TOP or (p.parts[0] in FOLDERS and p.suffix in TEXT)


def check_blob(name, data):
    if not allowed(name) or len(data) > 1_000_000 or b'\0' in data:
        raise SystemExit(f'Outside public text-only scope: {name}')
    data.decode('utf-8-sig')
    if any(line.strip() in (b'-----BEGIN PRIVATE KEY-----', b'-----BEGIN OPENSSH PRIVATE KEY-----') for line in data.splitlines()):
        raise SystemExit(f'Private key material: {name}')


def main():
    names = git('ls-files', '-z').decode().strip('\0').split('\0')
    if not names or names == ['']:
        raise SystemExit('No staged/tracked files; stage the reviewed public files first')
    for name in names:
        check_blob(name, git('show', ':' + name))
    objects = git('rev-list', '--objects', '--all').decode().splitlines()
    seen = set()
    for row in objects:
        sha, _, name = row.partition(' ')
        if name and git('cat-file', '-t', sha).strip() == b'blob':
            if not allowed(name):
                raise SystemExit(f'Forbidden historical path: {name}')
            if sha not in seen:
                check_blob(name, git('cat-file', 'blob', sha))
                seen.add(sha)
    for path in (ROOT / 'site').rglob('*'):
        if path.is_file():
            name = path.relative_to(ROOT).as_posix()
            if name not in names:
                raise SystemExit(f'Untracked website payload: {name}')
    print(f'PASS: {len(names)} staged files and {len(seen)} historical blobs; no game assets')


if __name__ == '__main__':
    main()
