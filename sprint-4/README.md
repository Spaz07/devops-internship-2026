# Sprint 4 – Multi-Platform Container Build Pipelines

## Overview

This sprint uses GitHub Actions to automatically build and publish a Docker image to GitHub Container Registry (GHCR). The image supports both `linux/amd64` and `linux/arm64` architectures.

The automated build runs on GitHub-hosted runners, so a local Docker installation is not required to run the pipeline.

## Project Files

- `app.py` – Displays the Python version and container architecture.
- `Dockerfile` – Defines how the container image is built.
- `.github/workflows/docker-build.yml` – Automates building, tagging, and publishing the image.
- `proof/` – Contains screenshots of the successful build and published image.

## Build Process

1. GitHub Actions checks out the repository.
2. QEMU provides emulation support for additional architectures.
3. Docker Buildx builds the image for `linux/amd64` and `linux/arm64`.
4. The workflow authenticates with GHCR using GitHub's `GITHUB_TOKEN`.
5. The image is tagged and published to GHCR.
6. GitHub Actions cache reuses build layers when available.

## Image Registry and Tags

The image is published to:

`ghcr.io/<owner>/<repository>`

The workflow generates these tags:

- `latest` – Build from the default branch.
- `sha-<commit>` – Identifies the commit used for the build.
- `vX.Y.Z` – Version tag generated when a matching Git version tag is pushed, such as `v2.2.1`.

Pushing a matching Git version tag triggers the workflow to build and publish an image with that version tag.

## Authentication and Permissions

The workflow uses GitHub's automatically provided `GITHUB_TOKEN` and the `packages: write` permission to publish images to GHCR. No registry password is hardcoded in the workflow.

## Build Cache

The workflow uses GitHub Actions caching with `cache-from: type=gha` and `cache-to: type=gha,mode=max` to reuse build layers when possible.

## Proof of Execution

- [Successful GitHub Actions build](proof/github-actions-build-success.png)
- [Published image and multi-architecture details](proof/ghcr-multi-architecture.png)
