# Uptime Kuma

Use the quick start in the [README](../README.md). The deployment stores data in PVC `data` in namespace `uptime-kuma`, mounted at `/app/data`.

SQLite is selected explicitly with `UPTIME_KUMA_DB_TYPE=sqlite`, so the first page asks you to create an administrator rather than choose a database. This bundle does not configure MariaDB.

The default probes allow up to ten minutes for a fresh startup. An existing v1 database migration can take much longer: read [UPGRADING](UPGRADING.md) before moving data.

For LAN access, use your existing reverse proxy/Ingress controller with TLS and authentication configured in Kuma. Keep the setup page private until the administrator account exists. Do not expose the service just to finish setup.

HTTP and TCP monitoring are the baseline for this least-privilege deployment. ICMP ping, Docker socket monitoring, browser monitors, and privileged integrations are not covered by its tests. The container drops all capabilities; ICMP availability depends on the node's ping policy. Do not enable privileged mode to work around it. Evaluate any additional permission narrowly in your own overlay.

For logs and storage troubleshooting:

```sh
kubectl -n uptime-kuma get pods,pvc
kubectl -n uptime-kuma logs deployment/uptime-kuma
kubectl -n uptime-kuma describe pods
```

Upstream: [Uptime Kuma](https://github.com/louislam/uptime-kuma), [v1-to-v2 migration](https://github.com/louislam/uptime-kuma/wiki/Migration-From-v1-To-v2).
