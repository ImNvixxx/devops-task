#!/bin/bash

set -e

set -a
source .env
set +a

if [ $# -ne 1 ]; then
    echo "Usage: ./restore.sh <backup-file>"
    exit 1
fi

BACKUP_FILE=$1

docker compose exec -T postgres psql \
    -U "$POSTGRES_USER" \
    "$POSTGRES_DB" \
    < "$BACKUP_FILE"

echo "Database restored from $BACKUP_FILE"
