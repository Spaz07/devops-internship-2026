#!/usr/bin/env bash
set -uo pipefail

APP="sprint-7-app"
IMAGE="sprint-7-app"
PORT=8090
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
STATE="$SCRIPT_DIR/../state/active-version"
VERSION="${1:-}"
ROLLBACK_VERSION="v1.0"

if [[ -z "$VERSION" ]]; then
    echo "Usage: $0 <v1.0|v2.0|v2.0-broken>"
    exit 1
fi

if ! docker image inspect "$IMAGE:$VERSION" >/dev/null 2>&1; then
    echo "ERROR: Image $IMAGE:$VERSION does not exist."
    exit 1
fi

if [[ "$VERSION" != "$ROLLBACK_VERSION" ]] &&
   ! docker image inspect "$IMAGE:$ROLLBACK_VERSION" >/dev/null 2>&1; then
    echo "ERROR: Rollback image $IMAGE:$ROLLBACK_VERSION does not exist."
    exit 1
fi

ACTIVE_BEFORE="not-initialized"
if [[ -f "$STATE" ]]; then
    ACTIVE_BEFORE="$(cat "$STATE")"
fi
echo "Currently recorded active version: $ACTIVE_BEFORE"

start_container() {
    local version="$1"
    docker rm -f "$APP" >/dev/null 2>&1 || true

    local broken=false
    [[ "$version" == "v2.0-broken" ]] && broken=true

    docker run -d --name "$APP" \
        -p "127.0.0.1:$PORT:5000" \
        -e APP_VERSION="$version" \
        -e APP_BROKEN="$broken" \
        "$IMAGE:$version" >/dev/null
}

smoke_test() {
    local version="$1"
    local attempt

    for attempt in 1 2 3; do
        echo "Smoke test attempt $attempt/3 for $version"

        if curl -fsS --max-time 2 "http://127.0.0.1:$PORT/health" >/dev/null \
           && curl -fsS --max-time 2 "http://127.0.0.1:$PORT/api/status" >/dev/null; then
            echo "PASS: Both endpoints are healthy on $version"
            return 0
        fi

        echo "FAIL: Smoke tests did not pass"
        if [[ "$attempt" -lt 3 ]]; then
            sleep 5
        fi
    done

    return 1
}

rollback_to_v1() {
    echo "ALERT: Restoring known-good $ROLLBACK_VERSION"

    if ! start_container "$ROLLBACK_VERSION"; then
        echo "CRITICAL: Failed to start rollback version $ROLLBACK_VERSION"
        return 1
    fi

    if smoke_test "$ROLLBACK_VERSION"; then
        printf '%s\n' "$ROLLBACK_VERSION" > "$STATE"
        echo "ROLLBACK SUCCESS: Service recovered on $ROLLBACK_VERSION"
        return 0
    fi

    echo "CRITICAL: Rollback version $ROLLBACK_VERSION is unhealthy"
    return 1
}

mkdir -p "$(dirname "$STATE")"
echo "Deploying $VERSION"

if ! start_container "$VERSION"; then
    echo "ERROR: Container failed to start"
    if [[ "$VERSION" != "$ROLLBACK_VERSION" ]]; then
        rollback_to_v1 || exit 2
    fi
    exit 1
fi

if smoke_test "$VERSION"; then
    printf '%s\n' "$VERSION" > "$STATE"
    echo "DEPLOYMENT SUCCESS: $VERSION is now active"
    exit 0
fi

echo "ALERT: $VERSION failed verification; starting rollback"

if [[ "$VERSION" == "$ROLLBACK_VERSION" ]]; then
    echo "CRITICAL: Known-good baseline $ROLLBACK_VERSION failed verification."
    exit 2
fi

rollback_to_v1 || exit 2
echo "DEPLOYMENT FAILED: $VERSION rejected; restored $ROLLBACK_VERSION"
exit 1
