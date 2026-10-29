# Vaultwarden

Vaultwarden is an independent Bitwarden-compatible server. The old folder name `bitwarden` did not mean it deployed the official Bitwarden server.

## Private first-time setup

```sh
kubectl apply -k apps/vaultwarden
kubectl -n vaultwarden rollout status deployment/vaultwarden --timeout=600s
kubectl -n vaultwarden set env deployment/vaultwarden SIGNUPS_ALLOWED=true
kubectl -n vaultwarden rollout status deployment/vaultwarden --timeout=600s
kubectl -n vaultwarden port-forward service/vaultwarden 8080:8080
```

Open **http://localhost:8080** on the computer running port-forward, create your account, then stop port-forward with Ctrl+C. Localhost is a browser secure context. Plain HTTP on a LAN IP is not a suitable web-vault deployment.

Immediately close registration:

```sh
kubectl -n vaultwarden set env deployment/vaultwarden SIGNUPS_ALLOWED=false
kubectl -n vaultwarden rollout status deployment/vaultwarden --timeout=600s
```

Registration is briefly open to other cluster workloads during this step, so do this only on a trusted cluster. Invitations are disabled by default. There is no admin token or enabled admin panel in these manifests. Do not put real credentials in Git.

## LAN or remote use

Configure an HTTPS reverse proxy/Ingress with a valid certificate and WebSocket support, and set `DOMAIN` to your exact public HTTPS URL in a local Kustomize overlay. Do this before connecting clients. Supply SMTP credentials through a Kubernetes Secret if you need mail delivery, account verification, or invitations; the base does not configure SMTP. Kubernetes Secrets need suitable RBAC and encryption-at-rest in your cluster.

Data lives in PVC `data` in namespace `vaultwarden`, mounted at `/data`. Admin settings saved in an existing `config.json` can override environment settings; check them during migration. Review the [upstream deployment wiki](https://github.com/dani-garcia/vaultwarden/wiki) and [backup instructions](https://github.com/dani-garcia/vaultwarden/wiki/Backing-up-your-vault).

Tests verify startup, the web page, `/alive`, and retained files/database across pod replacement. They do not exercise real vault accounts, client synchronization, mail, or TLS. Before storing real passwords, test a backup and restore and verify your client connections.
