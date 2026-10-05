# Sprint 2 - Workflow Automation & Testing

## Project Structure

- `app.py` - Simple Python application with addition and subtraction functions.
- `test_app.py` - Unit tests written using pytest.
- `../.github/workflows/ci.yml` - GitHub Actions CI workflow.

## CI Workflow

The GitHub Actions workflow:

1. Runs on pushes to `main`.
2. Runs on pull requests.
3. Sets up Python 3.12.
4. Installs pytest, pytest-cov, and flake8.
5. Runs Flake8 for code quality checks.
6. Runs pytest with coverage.
7. Generates `coverage.xml`.
8. Uploads the coverage report as a GitHub Actions artifact.

## Local Testing

From the `sprint-2` directory:

```bash
pytest
flake8 app.py test_app.py
pytest --cov=app --cov-report=xml
```

CI workflow verified successfully through GitHub Actions.
