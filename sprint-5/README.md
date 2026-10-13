# Sprint 5 – Blue-Green Deployment & Health Verification

## Overview

This sprint implements Blue-Green deployment using Docker Compose, a Flask sample application, Nginx, and a Bash deployment script. It verifies the target environment's health before switching live traffic and keeps the current environment active if health checks fail.

## Requirements

- Docker Engine and Docker Compose plugin
- Git
- `curl` and Bash

## Directory Structure

```text
sprint-5/
├── app/
│   ├── app.py
│   └── Dockerfile
├── nginx/
│   ├── active-upstream.conf
│   └── nginx.conf
├── scripts/
│   └── deploy.sh
├── proof/
└── docker-compose.yml
```

## Setup and Run

Clone the repository and enter the sprint directory:

```bash
git clone https://github.com/Spaz07/devops-internship-2026.git
cd devops-internship-2026/sprint-5
```

Build and start both application environments and Nginx:

```bash
docker compose up -d --build
docker compose ps
```

The services are available at:

- Blue: `http://127.0.0.1:5001`
- Green: `http://127.0.0.1:5002`
- Nginx live endpoint: `http://127.0.0.1:8080`

Check both health endpoints and the active application:

```bash
curl http://127.0.0.1:5001/healthz
curl http://127.0.0.1:5002/healthz
curl http://127.0.0.1:8080/
```

Initially, Nginx routes live traffic to Blue (`blue-v1`).

## Deploy and Verify

Switch traffic to Green:

```bash
./scripts/deploy.sh green
curl http://127.0.0.1:8080/
```

Switch traffic back to Blue:

```bash
./scripts/deploy.sh blue
curl http://127.0.0.1:8080/
```

The deployment script checks the target's `/healthz` endpoint, updates the Nginx upstream, validates the configuration, reloads Nginx, and verifies the live application version. If health checks fail, the switch is aborted and the current environment continues serving traffic.

## Test Failed Health Check

Ensure Blue is active before testing:

```bash
./scripts/deploy.sh blue
```

In `docker-compose.yml`, change **Green's** `APP_HEALTHY` value from `"true"` to `"false"`. Then recreate Green:

```bash
docker compose up -d --force-recreate green
curl -i http://127.0.0.1:5002/healthz
```

The health endpoint should return HTTP 503. Attempt deployment:

```bash
./scripts/deploy.sh green
curl http://127.0.0.1:8080/
```

The deployment should abort after five failed health checks, and the live endpoint should still return `blue-v1`.

After testing, restore Green's `APP_HEALTHY` value to `"true"` and recreate the container:

```bash
docker compose up -d --force-recreate green
curl http://127.0.0.1:5002/healthz
```

## Cleanup

Stop and remove the containers and network:

```bash
docker compose down
```

## Proof

The `proof/` directory contains evidence of successful Blue-Green switching and the failed-health-check scenario. Screenshots or terminal logs should show the deployment result and the version served by Nginx.
