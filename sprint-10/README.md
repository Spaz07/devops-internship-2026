# Sprint 10 – Custom CI CLI Tool

## Overview

This sprint focuses on developing a custom Python CLI tool to interact with GitHub Actions through the GitHub REST API.

The tool automates common CI operations, allowing users to inspect workflow runs, manually trigger workflows, and retrieve job execution details directly from the terminal.

## Technologies Used

- Python – CLI implementation
- Argparse – Command-line argument parsing
- Requests – HTTP requests to GitHub REST API
- GitHub REST API – Workflow and job management
- Setuptools – CLI packaging and installation

## Structure

```text
sprint-10/
├── ci_cli.py          # Main CLI implementation
├── requirements.txt   # Python dependencies
├── pyproject.toml     # Project configuration and CLI entry point
├── setup.sh           # Automated environment setup
├── README.md          # Documentation
└── proof/             # Execution screenshots
```

## How It Works

The CLI provides three subcommands:

### 1. List Workflow Runs

```bash
ci-cli list-runs --repo OWNER/REPOSITORY
```

- Retrieves the latest five GitHub Actions workflow runs.
- Displays run ID, workflow name, branch, status and conclusion.
- Uses the GitHub Actions workflow runs API.

### 2. Trigger Workflow

```bash
ci-cli trigger --repo OWNER/REPOSITORY --workflow docker-build.yml --ref main
```

- Triggers a workflow using GitHub's `workflow_dispatch` API.
- Accepts the repository, workflow filename and branch.
- Returns HTTP 204 when GitHub accepts the dispatch request.

### 3. Retrieve Workflow Logs

```bash
ci-cli logs --repo OWNER/REPOSITORY --run-id RUN_ID
```

- Retrieves jobs and individual execution steps.
- Displays step status and execution duration.
- Highlights failed steps.
- Handles running and pending steps where timestamps may not be available.

## Implementation

### Authentication

The tool uses a GitHub Personal Access Token stored in the `GITHUB_TOKEN` environment variable.

Authentication is handled through HTTP request headers rather than hardcoding credentials.

### API Integration

The implementation uses Python Requests to communicate with the GitHub REST API.

Endpoints used:

- `GET /repos/{owner}/{repo}/actions/runs`
- `POST /repos/{owner}/{repo}/actions/workflows/{workflow}/dispatches`
- `GET /repos/{owner}/{repo}/actions/runs/{run_id}/jobs`

### Error Handling

- Checks whether the GitHub token is available.
- Handles unsuccessful API responses and HTTP errors.
- Handles missing timestamps for running and pending workflow steps.
- Prevents the CLI from crashing when step execution details are incomplete.

### Design Decisions

- Argparse was selected to implement a lightweight CLI with separate subcommands.
- Requests was used for straightforward REST API communication.
- The GitHub token is supplied through an environment variable to avoid exposing credentials in source code.
- Setuptools provides an editable installation and a `ci-cli` executable entry point.

## Run Locally

### Prerequisites

- Python 3
- pip
- GitHub Personal Access Token with Actions read/write access to the target repository

### Setup

```bash
cd sprint-10
chmod +x setup.sh
./setup.sh
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Configure authentication:

```bash
export GITHUB_TOKEN="your_github_token"
```

Verify installation:

```bash
ci-cli --help
```

## Testing

The following operations were tested:

| Test | Result |
|---|---|
| CLI installation | Passed |
| List latest five workflow runs | Passed |
| Manual workflow dispatch | Passed |
| Retrieve workflow jobs and steps | Passed |
| Step duration calculation | Passed |
| Running/pending step handling | Passed |
| Missing token handling | Passed |
| Invalid repository handling | Passed |
| Invalid run ID handling | Passed |

The Docker build workflow was manually triggered through the CLI. GitHub accepted the dispatch request (HTTP 204), and the workflow completed successfully, including the multi-platform image build and push.

## Proof

The following screenshots demonstrate the CLI installation, workflow listing, manual workflow triggering, job and step inspection, and error handling.

| Screenshot | Description |
|---|---|
| 01-cli-installation.png | CLI installation and available commands |
| 02-list-runs.png | Listing the latest five GitHub Actions workflow runs |
| 03-trigger-workflow.png | Manually triggering a GitHub Actions workflow |
| 04-workflow-logs.png | Inspecting workflow jobs, steps, statuses and durations |

All execution screenshots are available in the `proof/` directory.
