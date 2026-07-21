#!/bin/bash

set -e

set -a
source .env
set +a

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="backups/backup_${TIMESTAMP}.sql"

docker compose exec -T postgres pg_dump \
    -U "$POSTGRES_USER" \
    "$POSTGRES_DB" \
    > "$BACKUP_FILE"

echo "Backup created: $BACKUP_FILE"
