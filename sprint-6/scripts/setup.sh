#!/usr/bin/env bash
set -euo pipefail

CLUSTER_NAME="sprint-6"
ARGOCD_MANIFEST="https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml"

echo "Checking Kind cluster..."

if ! kind get clusters | grep -qx "$CLUSTER_NAME"; then
    kind create cluster --name "$CLUSTER_NAME"
else
    echo "Kind cluster '$CLUSTER_NAME' already exists."
fi

kubectl cluster-info --context "kind-${CLUSTER_NAME}"

echo "Creating Argo CD namespace if needed..."
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -

echo "Installing Argo CD..."
kubectl apply --server-side --force-conflicts \
    -n argocd -f "$ARGOCD_MANIFEST"

echo "Waiting for Argo CD deployments..."
kubectl wait --for=condition=Available deployment --all -n argocd --timeout=300s
kubectl rollout status statefulset/argocd-application-controller \
    -n argocd --timeout=300s

echo "Argo CD installation is ready."
echo "To access the UI, run:"
echo "kubectl port-forward svc/argocd-server -n argocd 8081:443"
