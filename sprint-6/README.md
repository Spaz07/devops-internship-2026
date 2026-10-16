# Sprint 6 – GitOps & Declarative Continuous Delivery

## Overview

Implemented GitOps using Kind, Kubernetes, and Argo CD. Argo CD monitors the GitHub repository and automatically synchronizes Kubernetes resources with the configuration stored in Git.

## Architecture

- **Kind:** Local Kubernetes cluster.
- **Argo CD:** Automates synchronization and self-healing.
- **Deployment:** Runs NGINX with three replicas.
- **Service:** Exposes the application internally.

## Prerequisites

Docker, Kind, kubectl, Git, and access to the GitHub repository.

## Setup

Clone the repository and enter its directory:

```bash
git clone https://github.com/Spaz07/devops-internship-2026.git
cd devops-internship-2026
```

Run the setup script from the repository root:

```bash
bash sprint-6/scripts/setup.sh
```

Connect the GitHub repository in the Argo CD UI under **Settings → Repositories**. Configure repository credentials with read access if authentication is required.

Create the Argo CD Application:

```bash
kubectl apply -f sprint-6/application.yaml
```

Access the UI by running:

```bash
kubectl port-forward svc/argocd-server -n argocd 8081:443
```

Open https://localhost:8081. Keep the port-forward command running while using the UI.

Retrieve the initial admin password:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
echo
```

Log in with username `admin` and the retrieved password.

## Testing and Results

- **Auto-sync:** Changed the replica count from 2 to 3 in Git and pushed commit `20077d7`. Argo CD updated the Deployment to three replicas without manually applying the changed manifest.
- **Self-healing:** Scaled the Deployment down to one replica. Argo CD restored it to three replicas.
- **Verification:** The Deployment reached `3/3` ready replicas, and the Application reported `Synced` and `Healthy`.

## Design Decisions

Git is the source of truth. Automated sync keeps the cluster updated with committed changes, while self-healing restores the declared state. Repository credentials are kept out of Git.

## Proof of Work

Screenshots are available in `proof/`:

- `argocd-healthy-synced.png` – Argo CD status.
- `gitops-auto-sync-commit.png` – Git commit history.
- `gitops-self-healing.png` – Self-healing test output.
