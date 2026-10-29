# Storage and backups

The maintained apps request a new `ReadWriteOnce` PVC named `data` in their own namespace. No StorageClass is hardcoded: the cluster default is used. Uptime Kuma requests 5Gi and Vaultwarden 2Gi. Provisioners may treat these as requests rather than enforced filesystem quotas.

Use writable local or block storage for SQLite. A local-path volume stays tied to its node and does not provide failover. Your CSI driver must support the access mode and UID/GID 1000 permissions; `fsGroup: 1000` cannot repair every filesystem or provisioner. Do not recursively change ownership of an unknown existing data directory.

## Choose a different class or size before installation

Create an overlay outside this repository (adjust the relative resource path):

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../kubernetes-manifests-arm64/apps/uptime-kuma
patches:
  - target:
      kind: PersistentVolumeClaim
      name: data
    patch: |-
      - op: add
        path: /spec/storageClassName
        value: YOUR_STORAGE_CLASS
      - op: replace
        path: /spec/resources/requests/storage
        value: 10Gi
```

Preview with `kubectl kustomize /path/to/overlay`, then apply with `kubectl apply -k /path/to/overlay`. StorageClass selection is effectively immutable after claim creation. Expansion depends on driver support; shrinking is not supported.

## Pending or unwritable storage

```sh
kubectl get storageclass
kubectl -n uptime-kuma get pvc,pods
kubectl -n uptime-kuma describe pvc data
kubectl -n uptime-kuma get events --sort-by=.lastTimestamp
```

A `WaitForFirstConsumer` claim can remain pending until a pod is scheduled. Otherwise check the default class, capacity, provisioner logs, node affinity, and permissions. On a mixed architecture cluster, both images support ARM64 and AMD64; this repository does not target 32-bit ARM nodes.

## Back up and restore

Record the running image version and export deployment configuration without sharing secrets. For a simple consistent filesystem backup, stop the app (scale its deployment to zero), wait for its pod to terminate, and use your storage provider's snapshot/backup procedure to copy the entire data directory. Restart the app after the copy completes. Include attachments and keys, not just SQLite database files. Keep encrypted backups outside the node.

Restore into a separate test claim with the same app version and verify the contents before replacing your working instance. A PVC, `Retain` policy, or pod-restart test is not a backup. Check the PV's reclaim policy before removing claims; a dynamically provisioned volume commonly defaults to `Delete`.

The old NFS examples are preserved only in `legacy/`. They contain site-specific IPs, paths, and obsolete provisioner configuration. They are not a supported database storage option.
