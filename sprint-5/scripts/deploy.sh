
#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

UPSTREAM_FILE="$PROJECT_DIR/nginx/active-upstream.conf"
LIVE_URL="http://127.0.0.1:8080"
HEALTH_ATTEMPTS=5
HEALTH_DELAY=2

if [[ $# -ne 1 || ( "$1" != "blue" && "$1" != "green" ) ]]; then
    echo "Usage: $0 blue|green"
    exit 1
fi

TARGET="$1"
EXPECTED_VERSION="${TARGET}-v1"
[[ "$TARGET" == "green" ]] && EXPECTED_VERSION="green-v2"

CURRENT="$(grep -Eo 'server (blue|green):5000;' "$UPSTREAM_FILE" |
    awk '{print $2}' | cut -d: -f1)"

if [[ "$CURRENT" == "$TARGET" ]]; then
    echo "ERROR: $TARGET is already active."
    exit 1
fi

if [[ "$TARGET" == "blue" ]]; then
    TARGET_PORT=5001
else
    TARGET_PORT=5002
fi

echo "Current environment: $CURRENT"
echo "Deployment target:   $TARGET"
echo "Checking target health..."

HEALTHY=false
for ((i=1; i<=HEALTH_ATTEMPTS; i++)); do
    if [[ "$(curl -s -o /dev/null -w '%{http_code}' \
        "http://127.0.0.1:${TARGET_PORT}/healthz" || true)" == "200" ]]; then
        HEALTHY=true
        break
    fi
    echo "Health check $i/$HEALTH_ATTEMPTS failed."
    sleep "$HEALTH_DELAY"
done

if [[ "$HEALTHY" != "true" ]]; then
    echo "DEPLOYMENT ABORTED: $TARGET failed health checks."
    echo "Live traffic remains on $CURRENT."
    exit 1
fi

echo "Health check passed."

TEMP_FILE="$(mktemp "$PROJECT_DIR/nginx/active-upstream.XXXXXX")"
BACKUP_FILE="$(mktemp "$PROJECT_DIR/nginx/active-backup.XXXXXX")"
cp "$UPSTREAM_FILE" "$BACKUP_FILE"

cleanup() {
    rm -f "$TEMP_FILE" "$BACKUP_FILE"
}
trap cleanup EXIT

printf 'upstream app_backend {\n    server %s:5000;\n}\n' \
    "$TARGET" > "$TEMP_FILE"

mv "$TEMP_FILE" "$UPSTREAM_FILE"

if ! docker compose exec -T nginx nginx -t; then
    echo "Nginx configuration invalid. Restoring $CURRENT."
    cp "$BACKUP_FILE" "$UPSTREAM_FILE"
    exit 1
fi

if ! docker compose exec -T nginx nginx -s reload; then
    echo "Nginx reload failed. Restoring $CURRENT."
    cp "$BACKUP_FILE" "$UPSTREAM_FILE"
    docker compose exec -T nginx nginx -t &&
        docker compose exec -T nginx nginx -s reload || true
    exit 1
fi

echo "Verifying live traffic..."


LIVE_OK=false

for ((i=1; i<=5; i++)); do
    if curl --silent --fail "$LIVE_URL/" | grep -q "$EXPECTED_VERSION"; then
        LIVE_OK=true
        break
    fi

    echo "Live verification attempt $i/5 failed."
    sleep 1
done

if [[ "$LIVE_OK" == "true" ]]; then
    echo "SUCCESS: Live traffic now reaches $TARGET ($EXPECTED_VERSION)."
    exit 0
fi


echo "Live verification failed. Rolling back to $CURRENT."
cp "$BACKUP_FILE" "$UPSTREAM_FILE"

if docker compose exec -T nginx nginx -t; then
    docker compose exec -T nginx nginx -s reload
    echo "Rollback configuration restored to $CURRENT."
else
    echo "CRITICAL: Restored configuration failed validation."
    exit 1
fi

exit 1
