# Sprint 7 – Resilient Deployment Pipelines & Automated Rollbacks

## Overview

This sprint demonstrates resilient Docker deployments using automated HTTP smoke tests and rollback logic. A deployment is accepted only when the application passes its health checks. If a release fails verification, the script rejects it and restores the known-good `v1.0` baseline.

## Architecture

- **Flask application:** Provides `/health` and `/api/status` endpoints.
- **Docker images:** `v1.0` is the healthy baseline, `v2.0` is the healthy update, and `v2.0-broken` simulates a failed release by returning HTTP 500.
- **Deployment script:** `scripts/deploy.sh` starts the requested version, performs smoke tests, records the active version, and handles rollback.
- **State file:** `state/active-version` stores the active image tag after a successful deployment or recovery.
- **GitHub Actions:** Automatically tests healthy deployment and rollback scenarios.

### Deployment Flow

1. Deploy the requested image.
2. Test `/health` and `/api/status`, allowing up to three attempts with a five-second delay between failed attempts.
3. If both endpoints pass, record the deployed version as active.
4. If verification fails, restore `v1.0`, verify its health, record the recovered version, and report the rejected deployment.

## Prerequisites

- Docker Engine
- Bash
- `curl`
- Git and access to the repository

The local deployment uses port `8090`. Ensure it is available before running the deployment script.

## Setup and Execution

Run all commands from the repository root.

### 1. Build the Docker images

```bash
docker build -t sprint-7-app:v1.0 ./sprint-7/app
docker build -t sprint-7-app:v2.0 ./sprint-7/app
docker build -t sprint-7-app:v2.0-broken ./sprint-7/app
```

Each tag is used to test a different deployment scenario. The broken behavior is enabled by the deployment script when it starts `v2.0-broken`.

### 2. Deploy the healthy baseline

```bash
bash sprint-7/scripts/deploy.sh v1.0
```

**Expected result:** Smoke tests pass and `v1.0` is recorded as the active version.

### 3. Test a healthy update

```bash
bash sprint-7/scripts/deploy.sh v2.0
```

**Expected result:** Both endpoints pass their smoke tests, and the active-version state is updated to `v2.0`.

### 4. Simulate a failed release

```bash
bash sprint-7/scripts/deploy.sh v2.0-broken
```

**Expected result:** The broken version fails its smoke tests. The script reports the failure, restores `v1.0`, verifies that both endpoints are healthy, and records the recovered version.

The deployment command exits with a failure status when the requested release is rejected, even if rollback succeeds. This distinguishes a failed release from a successful recovery.

### 5. Verify the recovered service

After the rollback test, run:

```bash
cat sprint-7/state/active-version
curl -fsS http://127.0.0.1:8090/health
curl -fsS http://127.0.0.1:8090/api/status
```

**Expected result:** The state file contains `v1.0`, and both endpoints return successful HTTP responses.

## State Tracking and Design Decisions

The `state/active-version` file tracks the version accepted as active. It is updated only after successful smoke tests, including verification after rollback. The file is excluded from Git because it represents runtime deployment state rather than source configuration.

The sprint specifies `v1.0` as the known-good rollback baseline. Smoke-test retries help accommodate application startup delays, while the broken image demonstrates how a failed release is detected and rejected.

## GitHub Actions

The workflow is located at `.github/workflows/sprint-7-rollback.yml`.

- **Automatic execution:** Push changes to `main` under `sprint-7/` or modify the Sprint 7 workflow file.
- **Manual execution:** Open the repository's **Actions** tab, select **Sprint 7 - Resilient Deployment and Rollback**, and choose **Run workflow**.

The workflow runs two independent jobs:

- **Healthy deployment:** Deploys `v1.0`, updates to `v2.0`, and verifies that `v2.0` remains active and healthy.
- **Rollback test:** Deploys `v1.0`, attempts the broken release, and verifies that the service recovers to `v1.0`.

Each job builds its own images and runs on a separate GitHub-hosted runner.

## Proof of Work

The `proof/` directory contains terminal screenshots demonstrating the deployment scenarios:

- `execution-1.png` – Successful deployment of `v1.0`.
- `execution-2.png` – Successful deployment of `v2.0`.
- `execution-3.png` – Failed smoke tests for `v2.0-broken` and successful rollback to `v1.0`.

The GitHub Actions run provides additional automated verification of both healthy deployment and rollback behavior.
