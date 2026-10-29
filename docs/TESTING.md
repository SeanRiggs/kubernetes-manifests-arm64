# Validation and disposable-cluster tests

Static checks need Python 3 and PyYAML:

```sh
python3 -m pip install PyYAML==6.0.3
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

The strict YAML loader rejects duplicate keys, including the missing document separators in an original NFS example. Regression tests also cover correctly separated documents and an invalid claim reference. Maintained bundles are checked for service/selector/port relationships, storage references, one-writer update strategy, versioned images, probes, and container permissions. Historical `.example` files are intentionally excluded.

GitHub Actions creates a disposable kind v0.33.0 cluster running Kubernetes v1.35.8 on each of native AMD64 and ARM64 runners. It validates the rendered Kustomize resources against the Kubernetes API, then checks application startup, HTTP responses, UID 1000, database creation, and retained data after deleting and replacing each application pod. No cluster credentials or repository secrets are required. Logs and events are uploaded even on failure.

To reproduce, install Docker, kind, kubectl and the Python dependency above, create an expendable kind cluster, then run:

```sh
kind create cluster --wait 180s --image kindest/node:v1.35.8@sha256:07b2536e30b803ed61d1677a79df6115f798ce64c80f9e22f6ed45afd09323c0
SMOKE_TEST_DISPOSABLE=yes bash scripts/smoke.sh
kind delete cluster
```

Check your kubectl context first. The script creates namespaces and deletes application pods; never point it at an existing installation. Use the workflow's verified kind binary versions for an equivalent run.

These are fresh-install smoke tests, not a full application acceptance suite. They do not test physical Raspberry Pis, a particular K3s installation, host power loss, NFS, old database migration, mail, real password vaults, ingress/TLS, or multi-node storage failover. A successful pod replacement proves retained data on the same test cluster, not a backup or disaster recovery plan. CI does not publish images or deploy to any user's cluster.
