# Sprint 4 – Multi-Platform Container Build Pipelines

## Overview
This sprint focuses on automating multi-platform container image builds and publishing using Docker Buildx, QEMU, and GitHub Actions. Images are published to GitHub Container Registry (GHCR) for `linux/amd64` and `linux/arm64` architectures.

## Technologies Used
- Docker and Docker Buildx
- QEMU
- GitHub Actions
- GitHub Container Registry (GHCR)

## Implementation
The workflow is defined in `.github/workflows/docker-build.yml`, and the container-related files are maintained in `sprint-4/`.

The workflow configures QEMU and Docker Buildx, authenticates to GHCR using GitHub's automatically provided `GITHUB_TOKEN`, and builds and publishes images for both target architectures. It also uses GitHub Actions caching with `cache-from` and `cache-to` to reuse build layers and improve efficiency.

## Dynamic Tagging
The workflow generates image tags according to its configuration:

- `latest` – Identifies the latest published image under the configured tagging rules.
- `sha-xxxxxxx` – Identifies an image using its short commit SHA.
- `v1.0.0` – Identifies a versioned image when a corresponding release tag is used.

## Setup and Usage
1. Clone the repository and navigate to its root directory.
2. Ensure GitHub Actions is enabled and the workflow has the required permissions.
3. Push changes to the configured branch or use a supported release-tag trigger.
4. Open the repository's **Actions** tab to view the workflow run and logs.
5. Open the repository's **Packages** section to access the published GHCR image.

The image follows this naming format:

`ghcr.io/<owner>/<repository>`

## Proof of Work
The `proof/` folder contains screenshots of the successful GitHub Actions workflow run and the published GHCR package.
