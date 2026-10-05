# Sprint 2 - Workflow Automation & Testing

## Overview

This sprint implements a GitHub Actions CI workflow for a simple Python application.

The CI pipeline automatically performs code-quality checks, unit tests, test coverage generation, and coverage artifact upload whenever code is pushed to the `main` branch or a pull request is created or updated.

## Project Structure

```text
devops-internship-2026/
├── .github/
│   └── workflows/
│       └── ci.yml
└── sprint-2/
    ├── app.py
    ├── test_app.py
    ├── README.md
    └── proof/
        ├── ci-success.png
        └── ci-steps.png
```

### Files

* `app.py` - Contains the Python application functions.
* `test_app.py` - Contains unit tests written using pytest.
* `../.github/workflows/ci.yml` - Defines the GitHub Actions CI pipeline.
* `README.md` - Documents setup, testing, workflow structure, and design decisions.
* `proof/` - Contains screenshots showing successful CI execution.

## Prerequisites

The following are required to run the application and tests locally:

* Python 3.12 or later
* Git
* Internet connection for installing Python packages

GitHub Actions runs the workflow using Python 3.12 on an Ubuntu runner.

## Local Setup

Clone the repository and enter the Sprint 2 directory:

```bash
git clone https://github.com/Spaz07/devops-internship-2026.git
cd devops-internship-2026/sprint-2
```

Create a Python virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install the required testing and code-quality tools:

```bash
python -m pip install pytest pytest-cov flake8
```

## Local Testing

### 1. Run Unit Tests

```bash
pytest
```

This discovers and runs the unit tests in `test_app.py`.

### 2. Run Flake8

```bash
flake8 app.py test_app.py
```

This checks the application and test files for Python code-quality and PEP8 issues.

A successful run produces no output and returns to the terminal prompt.

### 3. Run Tests with Coverage

```bash
pytest --cov=app --cov-report=xml
```

This runs the unit tests and generates a `coverage.xml` report.

The coverage report shows which lines of the application were executed by the tests.

## CI Workflow

The workflow is located at:

```text
.github/workflows/ci.yml
```

The workflow is triggered automatically by:

* A push to the `main` branch.
* A pull request.

The pipeline performs the following steps:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Installs `pytest`, `pytest-cov`, and `flake8`.
4. Runs Flake8 on the application and test files.
5. Runs pytest with coverage enabled.
6. Generates `coverage.xml`.
7. Uploads `coverage.xml` as a GitHub Actions artifact.

If Flake8 reports an error or a pytest test fails, the workflow fails.

## Workflow Architecture

```text
Code Push / Pull Request
          |
          v
   GitHub Actions
          |
          v
   Checkout Repository
          |
          v
     Setup Python
          |
          v
 Install CI Dependencies
          |
          +----------------+
          |                |
          v                v
       Flake8           Pytest
                           |
                           v
                       Coverage
                           |
                           v
                    coverage.xml
                           |
                           v
                  Upload Artifact
```

## Design Decisions

* **pytest** is used for simple and readable automated unit testing.
* **pytest-cov** is used to generate test coverage information.
* **Flake8** is used to enforce basic Python code-quality and PEP8 checks.
* **GitHub Actions** is used to automate the checks so they run automatically after code changes are pushed.
* The coverage report is uploaded as an artifact so it can be downloaded from the completed GitHub Actions run.
* The local Python virtual environment is not committed to the repository; each user creates their own environment.
* The workflow uses a GitHub-hosted Ubuntu runner so the CI environment is independent of the developer's local machine.

## CI Verification

The CI workflow was verified by pushing changes to the `main` branch.

GitHub Actions automatically started the `Python CI` workflow after the push and completed successfully.

The successful workflow run verified:

* Flake8 passed.
* Unit tests passed.
* Test coverage was generated.
* The coverage report was uploaded as a GitHub Actions artifact.

The verification run produced 100% line coverage for the application.

## Proof of Work

Screenshots of the successful GitHub Actions CI run are available in the `proof/` directory:

* `proof/ci-success.png` - Shows the completed successful CI workflow run.
* `proof/ci-steps.png` - Shows the individual CI workflow steps completing successfully.

