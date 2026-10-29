# Kubernetes homelab manifests — ARM64 and AMD64

Small, understandable Kubernetes deployments for a home server or Raspberry Pi cluster. Each maintained app includes its own namespace, persistent storage claim, health probes, resource limits, and an internal service.

[![Validate and smoke test](https://github.com/SeanRiggs/kubernetes-manifests-arm64/actions/workflows/validate.yml/badge.svg)](https://github.com/SeanRiggs/kubernetes-manifests-arm64/actions/workflows/validate.yml)

## What is maintained?

| Application | Image version | Start here |
| --- | --- | --- |
| Uptime Kuma | 2.5.8 | [Monitoring setup](docs/UPTIME-KUMA.md) |
| Vaultwarden | 1.37.4 | [Password manager setup](docs/VAULTWARDEN.md) |

The original Booksonic Air, EmulatorJS, Bitwarden-named Vaultwarden, and storage examples are preserved in [legacy](legacy/README.md). LinuxServer has deprecated its Booksonic Air and EmulatorJS images; those deployments are historical references, not maintained installs. Existing users should read [the migration guide](docs/UPGRADING.md) before applying anything.

## First deployment: Uptime Kuma

You need an existing Kubernetes cluster, `kubectl` configured for it, and a default StorageClass that provisions writable local or block storage. K3s with its default local-path provisioner is one option. A 64-bit Linux server works too; Raspberry Pi hardware is not required. These files do not install Kubernetes.

```sh
git clone https://github.com/SeanRiggs/kubernetes-manifests-arm64.git
cd kubernetes-manifests-arm64
kubectl config current-context
kubectl get nodes -o wide
kubectl get storageclass
kubectl apply -k apps/uptime-kuma
kubectl -n uptime-kuma rollout status deployment/uptime-kuma --timeout=600s
kubectl -n uptime-kuma port-forward service/uptime-kuma 3001:3001
```

Open **http://localhost:3001** on the computer running port-forward and create your administrator account. Keep the terminal open. The service is internal to your cluster; port-forward listens on localhost by default. Follow the app guide for LAN access.

## Storage and safety

- Each app runs one replica with a `Recreate` update strategy. This avoids overlapping database writers during upgrades; it is not high availability.
- SQLite data belongs on local or block storage, not NFS/SMB. [Storage guide](docs/STORAGE.md) covers customization, backups, and pending claims.
- Containers run as UID/GID 1000 without privileged mode or a service-account token. No root permission-fixing container is included.
- Services are `ClusterIP`. Ingress, TLS, DNS, and network access policies depend on your cluster and must be configured separately. ClusterIP does not isolate an app from other cluster workloads.
- Do not delete a namespace or PVC as an uninstall shortcut: your StorageClass may delete the underlying data. Back up first.
- Apply one app with `kubectl apply -k apps/<app>`; never recursively apply the repository root.

## Test and contribute

[Testing](docs/TESTING.md) explains static validation and disposable Kubernetes tests on native AMD64 and ARM64 runners. Tests cover fresh startup, HTTP health, non-root execution, and data persistence across pod replacement. They do not certify Raspberry Pi hardware, existing database upgrades, storage failure recovery, or complete password-manager workflows.

Have a useful homelab app or a better deployment? See [CONTRIBUTING.md](CONTRIBUTING.md). Keep examples portable, document storage and upgrade behavior, and bring a reproducible test. Report problems through [GitHub issues](https://github.com/SeanRiggs/kubernetes-manifests-arm64/issues), with secrets removed.
