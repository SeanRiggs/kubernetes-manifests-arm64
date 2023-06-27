# code-server Helm chart

This Helm chart deploys [code-server](https://github.com/coder/code-server), a web-based IDE that runs on Kubernetes.

## TL;DR

$ helm repo add nicholaswilde <https://nicholaswilde.github.io/helm-charts/>
$ helm repo update
$ helm install code-server nicholaswilde/code-server

Uninstalling the Chart
To uninstall the code-server deployment:

helm uninstall code-server

with Values:

helm install code-server nicholaswilde/code-server -f values.yaml
