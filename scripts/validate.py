"""Reject ambiguous YAML and broken relationships in maintained app bundles."""
from pathlib import Path
import yaml

class StrictLoader(yaml.SafeLoader):
    pass

def mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f'duplicate YAML key: {key} at line {key_node.start_mark.line + 1}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result

StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)

def documents(text):
    return list(yaml.load_all(text, Loader=StrictLoader))

def validate(folder):
    docs = documents((folder / 'resources.yaml').read_text())
    kinds = {d['kind']: d for d in docs}
    assert len(kinds) == len(docs) == 4, 'expected one namespace, claim, deployment and service'
    dep, svc, pvc = [kinds[k] for k in ('Deployment', 'Service', 'PersistentVolumeClaim')]
    spec = dep['spec']; pod = spec['template']['spec']; labels = spec['template']['metadata']['labels']
    assert spec['replicas'] == 1 and spec['strategy']['type'] == 'Recreate'
    assert spec['selector']['matchLabels'] == svc['spec']['selector'] == labels
    assert svc['spec']['type'] == 'ClusterIP'
    assert pod['automountServiceAccountToken'] is False
    assert pod['securityContext']['runAsNonRoot'] is True
    assert pod['securityContext']['runAsUser'] > 0
    for v in pod['volumes']:
        assert v['persistentVolumeClaim']['claimName'] == pvc['metadata']['name'], 'unbound claim reference'
    assert pvc['spec']['accessModes'] == ['ReadWriteOnce']
    for c in pod['containers']:
        assert ':' in c['image'] and not c['image'].endswith(':latest'), 'unpinned image'
        assert not c['securityContext'].get('privileged', False)
        assert c['securityContext']['allowPrivilegeEscalation'] is False
        for p in ('startupProbe', 'readinessProbe', 'livenessProbe'):
            assert p in c
        ports = {p['name'] for p in c['ports']}
        assert all(p['targetPort'] in ports for p in svc['spec']['ports'])
    kust = documents((folder / 'kustomization.yaml').read_text())[0]
    assert kust['namespace'] == kinds['Namespace']['metadata']['name'] == folder.name
    assert kust['resources'] == ['resources.yaml']

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    for folder in sorted((root / 'apps').iterdir()):
        validate(folder)
        print(f'Validated {folder.name}')
    for workflow in (root / '.github/workflows').glob('*.yml'):
        documents(workflow.read_text())
        print(f'Validated YAML: {workflow.name}')
