# Sprint 9 — Serverless Deployment Automation & Packaging

## Overview

This sprint implements a serverless Items API using Python and AWS SAM. The application is packaged, deployed, and tested through GitHub Actions using LocalEmu to emulate AWS services locally, without requiring a paid AWS account.

## Architecture

- **AWS SAM:** Defines and packages the serverless resources.
- **AWS Lambda:** Runs the Python functions.
- **API Gateway:** Exposes the HTTP endpoints.
- **DynamoDB:** Stores the items.
- **LocalEmu:** Emulates AWS services for local deployment and testing.

### API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/items` | Retrieves stored items |
| POST | `/items` | Creates an item from a JSON request body |

Example POST body:

```json
{"name": "Book"}
```

A successful POST returns `201 Created`, and GET returns `200 OK`.

## Prerequisites

- Python 3.12
- Docker and Docker Compose
- AWS SAM CLI

## Local Setup and Deployment

Run commands from the repository root.

**1. Install dependencies and run unit tests**

```bash
python3 -m venv .venv
.venv/bin/pip install pytest -r sprint-9/src/requirements.txt
.venv/bin/python -m pytest sprint-9/tests -v
```

**2. Validate and build the application**

```bash
.venv/bin/sam validate --template-file sprint-9/template.yaml
.venv/bin/sam build --template-file sprint-9/template.yaml
```

**3. Start LocalEmu**

```bash
docker compose -f sprint-9/docker-compose.yml up -d
```

**4. Configure local credentials**

These dummy credentials are for local emulation only; they are not real AWS credentials.

```bash
export AWS_ENDPOINT_URL=http://localhost:4566
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
```

Create the S3 bucket used for deployment artifacts:

```bash
docker exec sprint-9-localemu sh -lc \
  '. /opt/code/localemu/.venv/bin/activate && awsemu s3 mb s3://sprint-9-artifacts'
```

**5. Package and deploy**

```bash
.venv/bin/sam package \
  --template-file .aws-sam/build/template.yaml \
  --s3-bucket sprint-9-artifacts \
  --output-template-file .aws-sam/packaged.yaml

.venv/bin/sam deploy \
  --template-file .aws-sam/packaged.yaml \
  --stack-name sprint-9 \
  --s3-bucket sprint-9-artifacts \
  --capabilities CAPABILITY_IAM \
  --no-confirm-changeset
```

## GitHub Actions CI/CD

The workflow is defined in `.github/workflows/sprint-9-serverless.yml`. It runs when Sprint 9 files change or when manually triggered.

The pipeline:
1. Runs unit tests and validates the SAM template.
2. Builds and packages the application.
3. Uploads the packaged template as a workflow artifact.
4. Deploys the stack through CloudFormation using LocalEmu.
5. Tests the deployed API and verifies that a created item can be retrieved from DynamoDB.

The successful workflow verified `POST 201`, `GET 200`, and item persistence.

## Proof of Execution

Screenshots from the successful GitHub Actions run:

- [Workflow success](proof/ci-success.png)
- [Workflow steps](proof/ci-steps.png)
- [Packaging](proof/packaging.png)
- [Deployment](proof/deployment.png)
- [API integration tests](proof/api-integration.png)
