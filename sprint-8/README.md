# Sprint 8 – Performance Testing with k6

## Overview

This sprint demonstrates automated performance testing using Grafana k6. A Flask API runs in Docker, and k6 generates requests to measure response times and verify performance thresholds.

The goal is to ensure that a healthy application passes performance checks while an application with excessive latency is rejected by the performance gate.

## Implementation

The Flask application provides health, sample-items, and data endpoints. The k6 test sends requests with up to 10 virtual users and checks:

- 95th-percentile response time below 200 ms.
- HTTP request failure rate below 1%.
- Successful HTTP responses from the tested endpoints.

Artificial latency can be enabled through the `API_DELAY` environment variable to simulate a slow application.

## Running the Tests

Build and start the application from the repository root:

```bash
docker build -t sprint-8-app:latest ./sprint-8/app

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

Run the same k6 command again. The test should fail because the response-time threshold is exceeded, even though the API may still return HTTP 200.

## GitHub Actions

The workflow at `.github/workflows/sprint-8-performance.yml` automates both scenarios when relevant Sprint 8 files change on pushes or pull requests targeting `main`. It can also be triggered manually.

The workflow passes when the healthy application passes its performance test and the slow application is correctly rejected by the latency threshold.

## Proof

- [Baseline test – Passed](proof/baseline-pass.png)
- [Latency test – Threshold failure expected](proof/latency-fail.png)

The successful GitHub Actions run also confirms that the performance gate behaves as expected.
