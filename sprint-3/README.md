# Sprint 3 – Release Automation & Release Engineering

## Overview

This sprint implements automated release management using GitHub Actions and `semantic-release`.

The workflow analyzes Git commit messages, determines the next Semantic Version, creates a Git tag, generates GitHub Release notes, and attaches a release artifact.

## Architecture

The release process consists of:

1. Changes are committed and pushed to the `main` branch.
2. GitHub Actions starts the release workflow.
3. `semantic-release` analyzes commits since the previous release.
4. The commit type determines the version increment.
5. A Git tag is automatically created.
6. GitHub Release notes are generated.
7. The Sprint 3 application is packaged as `release.tar.gz`.
8. The tarball is attached to the GitHub Release.

### Main Components

* `sprint-3/app.py` – Sample log analysis application.
* `sprint-3/sample.log` – Sample input log.
* `.github/workflows/release.yml` – GitHub Actions release workflow.
* `package.json` – Defines the semantic-release dependency.
* `.releaserc.json` – Configures semantic-release and the release artifact.

## Prerequisites

* Git
* GitHub repository
* GitHub Actions enabled
* Node.js and npm are provided by the GitHub Actions runner.
* `semantic-release` is installed automatically by the workflow.

## Release Versioning

The release version is determined from commit messages.

| Commit format                               | Version change |
| ------------------------------------------- | -------------- |
| `fix:`                                      | Patch          |
| `feat:`                                     | Minor          |
| Commit containing `BREAKING CHANGE:` footer | Major          |

### Examples

Patch release:

```text
fix: improve log analyzer usage message
```

Minor release:

```text
feat: add summary command option
```

Major release:

```text
feat: change command interface

BREAKING CHANGE: the log analyzer now requires the --file option.
```

The version number is generated automatically. The version does not need to be specified manually.

## Application

The Sprint 3 application analyzes a log file and counts:

* Total lines
* Errors
* Warnings

Run it with:

```bash
python3 sprint-3/app.py --file sprint-3/sample.log
```

The application also supports the summary option:

```bash
python3 sprint-3/app.py --summary sprint-3/sample.log
```

## Release Workflow

The workflow runs automatically when changes are pushed to the `main` branch.

The workflow:

1. Checks out the repository with full Git history.
2. Sets up Node.js.
3. Installs semantic-release dependencies.
4. Creates `release.tar.gz` containing the Sprint 3 application.
5. Runs semantic-release.
6. Creates the Git tag and GitHub Release when a release is required.

## Release Artifact

Each generated release contains:

```text
release.tar.gz
```

The archive contains the Sprint 3 application files.

## Proof of Work

Automated releases were successfully tested with:

* `v1.0.0` – minor release from `feat:`
* `v1.0.1` – patch release from `fix:`
* `v2.0.0` – major release using a `BREAKING CHANGE:` footer
* `v2.1.0` – minor release from `feat:`
* `v2.1.1` – patch release from `fix:`

Each successful release demonstrates automated versioning, Git tagging, release notes generation, and release artifact generation.

Screenshots of the generated GitHub Releases are included as Sprint 3 proof.

## Design Decisions

* GitHub Actions is used to automate the release process.
* `semantic-release` determines versions from commit history instead of manually specifying version numbers.
* Full Git history is checked out so semantic-release can identify commits since the previous release.
* The GitHub Actions `GITHUB_TOKEN` is used for release operations instead of storing a personal access token.
* The release artifact is generated during the workflow so the published asset matches the current repository state.
