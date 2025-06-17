#!/bin/bash
set -e
SITE=${SITE:-dev.localhost}
BACKUP_FILE=$1
if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup-file>" >&2
    exit 1
fi
bench --site "$SITE" --force restore "$BACKUP_FILE"
