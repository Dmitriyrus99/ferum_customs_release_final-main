#!/bin/bash
set -e
SITE=${SITE:-dev.localhost}
bench --site "$SITE" backup --with-files
