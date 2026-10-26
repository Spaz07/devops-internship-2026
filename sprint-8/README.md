# Sprint 8 – Continuous Performance Testing & SLA Gates

## Overview

This sprint integrates automated performance testing using Grafana k6 into GitHub Actions. A Flask API runs in Docker, and k6 simulates concurrent users to measure response times and verify service-level objectives (SLOs).

## Implementation

The application exposes:

- `GET /api/items` – retrieves sample items.
- `POST /api/data` – returns sample data and supports configurable artificial latency.
- `GET /health` – checks application health.

The k6 test ramps up to 20 virtual users over 30 seconds and tests both API endpoints.

**Performance thresholds:**
- 95th-percentile response time (`p(95)`) below 200 ms.
- HTTP request failure rate below 1%.

The `API_DELAY` environment variable introduces artificial latency to demonstrate the performance gate.

## Running Locally

Build the application image:

```bash
docker build -t sprint-8-app:latest ./sprint-8/app
```

Start the healthy application:

```bash
docker run -d --name sprint-8-app \
  -p 5000:5000 sprint-8-app:latest
```

Run the k6 test:

```bash
docker run --rm \
  --network host \
  -v "$PWD/sprint-8/k6:/scripts:ro" \
  grafana/k6 run /scripts/performance.js
```

To test the latency gate, restart the application with a one-second delay:

```bash
docker rm -f sprint-8-app

docker run -d --name sprint-8-app \
  -p 5000:5000 \
  -e API_DELAY=1 \
  sprint-8-app:latest
```

Run the same k6 command again. The performance threshold should fail because the response time exceeds 200 ms.

## GitHub Actions

The workflow is located at `.github/workflows/sprint-8-performance.yml`.

- **Healthy scenario:** runs automatically on relevant pushes and pull requests, and should pass when the SLOs are met.
- **Slow scenario:** select `slow` using the manual **Run workflow** option. The artificial delay causes the latency threshold to fail, making the workflow fail as expected.

## Proof

### Local k6 Tests

- [Healthy application – Passed](proof/baseline-pass.png)
- [Artificial latency – Threshold failure](proof/latency-fail.png)

### GitHub Actions CI Runs

- [Healthy CI run – Passed](proof/ci-healthy.png)
- [Slow application – CI latency gate failed](proof/ci-slow-failure.png)
