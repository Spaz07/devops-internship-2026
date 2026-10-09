
# Sprint 4 – Multi-Platform Container Build Pipelines

## Overview

This sprint demonstrates an automated Docker build pipeline using GitHub Actions, Docker Buildx, and QEMU. The pipeline builds and publishes a container image for both `linux/amd64` and `linux/arm64` architectures to GitHub Container Registry (GHCR).

## Project Files

- `app.py` – Displays the Python version and container architecture.
- `Dockerfile` – Defines the Python runtime and application startup command.
- `.github/workflows/docker-build.yml` – Automates the multi-platform build and publishing process.

## Build Process

1. GitHub Actions checks out the repository.
2. QEMU enables emulation for additional CPU architectures.
3. Docker Buildx prepares the multi-platform builder.
4. The workflow authenticates with GHCR using `GITHUB_TOKEN`.
5. Docker builds the image for `linux/amd64` and `linux/arm64`.
6. The image is pushed to GHCR with generated tags.
7. GitHub Actions build cache is used to improve subsequent builds.

## Image Registry

The image is published to:

`ghcr.io/<owner>/<repository>`

The repository and image name are derived automatically from the GitHub repository.

## Image Tags

The workflow supports these tags:

- `latest` – Latest build from the default branch.
- `sha-<commit>` – Image identified by a short commit SHA.
- `<version>` – Version tag, such as `v1.0.0`, when building from a Git tag.
- A manually supplied release tag can also be published using the workflow's `release_tag` input.

## Authentication and Permissions

The workflow uses GitHub's automatically provided `GITHUB_TOKEN` to authenticate with GHCR. The workflow has `packages: write` permission to publish container images. No registry password is stored in the source code.

## Multi-Platform Support

The image targets:

- `linux/amd64`
- `linux/arm64`

QEMU and Docker Buildx allow the workflow to build these architectures from the GitHub Actions runner.

## Build Cache

The pipeline uses GitHub Actions cache with `cache-from` and `cache-to` to reuse build layers and reduce build time where possible.

## Local Testing

Build the image:

```bash
sudo docker build -t sprint4-demo:test ./sprint-4
```

Run the container:

```bash
sudo docker run --rm sprint4-demo:test
```

The application prints its Python version and the architecture reported by the running container.

## Verification

After a successful GitHub Actions run:

1. Check the workflow run logs.
2. Open the repository's Packages section on GitHub.
3. Verify the published image tags.
4. Inspect the image manifest to confirm both target architectures are available.
