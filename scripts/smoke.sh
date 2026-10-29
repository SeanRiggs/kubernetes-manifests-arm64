#!/usr/bin/env bash
# Only run against a disposable cluster; creates namespaces and replaces pods.
set -euo pipefail
if [[ "${SMOKE_TEST_DISPOSABLE:-}" != yes ]]; then
  echo 'Set SMOKE_TEST_DISPOSABLE=yes only for an expendable test cluster.' >&2
  exit 1
fi
for app in uptime-kuma vaultwarden; do
  if [[ "$app" == uptime-kuma ]]; then port=3001; data=/app/data; health=/; db=kuma.db; else port=8080; data=/data; health=/alive; db=db.sqlite3; fi
  kubectl apply -f <(kubectl kustomize "apps/$app" | python3 -c 'import sys,yaml; print(yaml.safe_dump(next(d for d in yaml.safe_load_all(sys.stdin) if d["kind"] == "Namespace")))')
  kubectl apply --dry-run=server -k "apps/$app"
  kubectl apply -k "apps/$app"
  kubectl -n "$app" rollout status "deployment/$app" --timeout=600s
  uid=$(kubectl -n "$app" exec "deployment/$app" -- id -u)
  test "$uid" = 1000
  kubectl -n "$app" exec "deployment/$app" -- test -s "$data/$db"
  kubectl -n "$app" port-forward "service/$app" "18080:$port" > /tmp/port-forward.log 2>&1 &
  forward_pid=$!
  trap 'kill "$forward_pid" 2>/dev/null || true' EXIT
  curl --retry 20 --retry-all-errors --retry-delay 2 --max-time 10 --fail "http://127.0.0.1:18080$health" -o /tmp/health-response
  curl --fail --max-time 10 http://127.0.0.1:18080/ -o /tmp/web-response
  test -s /tmp/web-response
  kill "$forward_pid"; wait "$forward_pid" 2>/dev/null || true
  trap - EXIT
  marker="retained-$app-$RANDOM"
  kubectl -n "$app" exec "deployment/$app" -- sh -c 'printf "%s" "$1" > "$2/smoke-marker"' sh "$marker" "$data"
  old_uid=$(kubectl -n "$app" get pod -l "app.kubernetes.io/name=$app" -o jsonpath='{.items[0].metadata.uid}')
  kubectl -n "$app" delete pod -l "app.kubernetes.io/name=$app" --wait=true
  kubectl -n "$app" rollout status "deployment/$app" --timeout=600s
  new_uid=$(kubectl -n "$app" get pod -l "app.kubernetes.io/name=$app" -o jsonpath='{.items[0].metadata.uid}')
  test "$old_uid" != "$new_uid"
  test "$(kubectl -n "$app" exec "deployment/$app" -- cat "$data/smoke-marker")" = "$marker"
  kubectl -n "$app" exec "deployment/$app" -- test -s "$data/$db"
  kubectl -n "$app" exec "deployment/$app" -- rm "$data/smoke-marker"
  echo "PASS $app: startup, health, UID 1000, replacement pod, retained marker and database"
done
