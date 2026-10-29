import importlib.util
from pathlib import Path
import tempfile
import unittest
import yaml
s = importlib.util.spec_from_file_location('validate', Path(__file__).resolve().parents[1] / 'scripts/validate.py')
v = importlib.util.module_from_spec(s)
s.loader.exec_module(v)

class ValidationRegression(unittest.TestCase):
    def test_missing_document_separator_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate YAML key'):
            v.documents('apiVersion: v1\nkind: PersistentVolume\napiVersion: v1\nkind: PersistentVolumeClaim\n')

    def test_separate_documents_are_preserved(self):
        self.assertEqual(len(v.documents('kind: PersistentVolume\n---\nkind: PersistentVolumeClaim\n')), 2)

    def test_wrong_claim_is_rejected(self):
        app = Path(__file__).resolve().parents[1] / 'apps/uptime-kuma'
        docs = v.documents((app / 'resources.yaml').read_text())
        next(d for d in docs if d['kind'] == 'Deployment')['spec']['template']['spec']['volumes'][0]['persistentVolumeClaim']['claimName'] = 'missing'
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'uptime-kuma'; folder.mkdir()
            (folder / 'resources.yaml').write_text(yaml.safe_dump_all(docs))
            (folder / 'kustomization.yaml').write_text((app / 'kustomization.yaml').read_text())
            with self.assertRaisesRegex(AssertionError, 'unbound claim'):
                v.validate(folder)
