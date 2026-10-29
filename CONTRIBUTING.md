# Contributing

Bring a small, documented change with a reproducible test. For a new application, document its upstream image, architecture support, storage, ports, setup, upgrades, and backup/restore process. Pin an explicit release version; do not use `latest`. Keep credentials and site-specific addresses out of maintained manifests.

Run the checks in [docs/TESTING.md](docs/TESTING.md). Pull requests run static validation and disposable kind smoke tests; CI never deploys to a user's cluster. Image upgrades need both architecture jobs to pass and a review of upstream migration notes. A successful health check alone does not prove every application feature works.

Keep existing data safe when changing names, namespaces, or claims. Describe any manual migration steps. Historical examples under `legacy/` are intentionally not active deployments.
