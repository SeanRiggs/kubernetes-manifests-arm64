# Migrating from the original manifests

This refresh changes paths, namespaces, claim names, service exposure, container identity, and application versions. **It is not an in-place migration.** Applying a new bundle creates an empty installation; it does not discover or copy old data.

| Original path | Replacement |
| --- | --- |
| `manifests/kuma.yml` and `manifests/storage/kuma*.yml` | `apps/uptime-kuma` |
| `manifests/bitwarden/*` | `apps/vaultwarden` |
| Booksonic Air, EmulatorJS, all old storage examples | Historical copies under `legacy/manifests/`, with `.example` suffix |

1. Inventory the old deployment's actual namespace, image digest/version, volume mounts, PVC/PV bindings, filesystem paths, settings, and service IPs. The old Vaultwarden deployment referenced PVC `nfs`; do not assume the separately named PV/PVC file describes the data actually in use.
2. Back up all application data consistently while the old app is stopped. Preserve old manifests and exact image versions. Test the backup before upgrading.
3. Create a separate test installation and copy a backup into its new claim using your storage provider's restore process. Claims cannot be mounted across namespaces. Verify UID/GID 1000 write permissions without changing the original data.
4. Uptime Kuma changes from major version 1 to 2. Follow [upstream migration guidance](https://github.com/louislam/uptime-kuma/wiki/Migration-From-v1-To-v2). Data conversion may take hours. On the isolated migration copy, temporarily remove startup/readiness/liveness probes or increase their budgets sufficiently so Kubernetes cannot kill an in-progress migration. Restore normal probes once migration finishes. Never run v1 against a v2-converted database; roll back using the untouched backup and old image.
5. For Vaultwarden, read [release notes](https://github.com/dani-garcia/vaultwarden/releases) from your actual running version through 1.37.4. Check client compatibility, registration settings, `config.json`, domain, SMTP, keys, and attachments. Do not assume an image downgrade reverses schema changes.
6. Verify login, real app functions, and retained data in the isolated copy. Stop the original writer before final backup/cutover. Update reverse proxy targets: the new services are internal, namespaced, and Vaultwarden uses port 8080.
7. Keep the old volumes and backup until the new instance and a restore are proven. Do not run `kubectl delete -f` on old storage files or delete old namespaces as part of this migration.

LinuxServer's [Booksonic Air image](https://docs.linuxserver.io/deprecated_images/docker-booksonic-air/) and [EmulatorJS image](https://docs.linuxserver.io/deprecated_images/docker-emulatorjs/) are deprecated. This statement concerns those container images, not every related upstream project. Preserve their data and evaluate a maintained replacement separately; no automatic format conversion is provided here.
