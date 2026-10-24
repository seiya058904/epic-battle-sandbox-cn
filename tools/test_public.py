"""Regressions for public asset boundaries and non-destructive local imports."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import check_public
import import_originals


class PublicBoundaryTests(unittest.TestCase):
    def test_rejects_assets_even_under_site(self):
        for path, data in [('Build/EBS.loader.js', b'code'), ('index.html', b'upstream'),
                           ('site/game.data', b'asset'), ('site/game.wasm', b'wasm'),
                           ('site/screenshot.png', b'image'), ('tools/file.py', b'\0binary'),
                           ('site/large.js', b'x' * 1_000_001),
                           ('tools/key.txt', b'-----BEGIN PRIVATE KEY-----')]:
            with self.subTest(path=path), self.assertRaises(SystemExit):
                check_public.check_blob(path, data)

    def test_accepts_documentation_and_own_source(self):
        for name in ['site/index.html', 'site/banner.svg', 'tools/build_local.py',
                     '.github/workflows/pages.yml', 'README.md', 'local.html']:
            check_public.check_blob(name, '简体中文'.encode())

    def test_runtime_changes_need_explicit_hash_review(self):
        for name in check_public.ASSETS:
            with self.subTest(name=name), self.assertRaises(SystemExit):
                check_public.check_blob(name, b'unreviewed replacement')

    def test_readme_prose_is_english(self):
        root = Path(__file__).resolve().parents[1]
        for name in ('README.md', 'README_LOCAL.md'):
            text = (root / name).read_text(encoding='utf-8')
            self.assertFalse(any('\u3400' <= c <= '\u9fff' for c in text), name)

    def test_site_local_links_exist(self):
        root = Path(__file__).resolve().parents[1]
        class Links(HTMLParser):
            refs = []
            ids = set()
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if 'id' in attrs:
                    self.ids.add(attrs['id'])
                for key in ('href', 'src'):
                    if key in attrs:
                        self.refs.append(attrs[key])
        page = Links()
        page.feed((root / 'site/index.html').read_text(encoding='utf-8'))
        repo = 'https://github.com/seiya058904/epic-battle-sandbox-cn/blob/main/'
        for link in page.refs:
            with self.subTest(link=link):
                if link.startswith('#'):
                    self.assertIn(link[1:], page.ids)
                elif link.startswith(repo):
                    self.assertTrue((root / link[len(repo):]).is_file())
                elif not link.startswith('https://'):
                    if link.startswith('Build/'):
                        self.assertTrue((root / 'web-build' / Path(link).name).is_file())
                    else:
                        self.assertTrue((root / 'site' / link).exists() or (root / link).exists())


class ImportTests(unittest.TestCase):
    def test_valid_import_is_repeatable_and_bad_inputs_never_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            root, source = parent / 'project', parent / 'source'
            (root / 'evidence').mkdir(parents=True)
            source.mkdir()
            rows = []
            for name, data in [('one.txt', b'original-one'), ('two.txt', b'original-two')]:
                (source / name).write_bytes(data)
                rows.append({'path': name, 'sha256': hashlib.sha256(data).hexdigest()})
            (root / 'evidence/baseline-manifest.json').write_text(json.dumps({'files': rows}))
            with patch.object(import_originals, 'ROOT', root), patch('sys.argv', ['import', '--from-directory', str(source)]):
                (source / 'two.txt').write_bytes(b'wrong')
                with self.assertRaises(SystemExit):
                    import_originals.main()
                self.assertFalse((root / 'one.txt').exists())
                (source / 'two.txt').write_bytes(b'original-two')
                import_originals.main()
                import_originals.main()
                (root / 'one.txt').write_bytes(b'keep-my-file')
                with self.assertRaises(SystemExit):
                    import_originals.main()
                self.assertEqual((root / 'one.txt').read_bytes(), b'keep-my-file')
                self.assertEqual((parent / 'original-backup/one.txt').read_bytes(), b'original-one')


if __name__ == '__main__':
    unittest.main()
