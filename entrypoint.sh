#!/bin/bash
set -e

BENCH_FOLDER="${BENCH_FOLDER:-frappe-bench}"

if [ ! -d "$BENCH_FOLDER" ]; then
    /bootstrap.sh
fi

cd "$BENCH_FOLDER"

if [[ "$1" == "pytest" ]]; then
    shift
    bench --site "${SITE_NAME:-dev.localhost}" run-tests --app ferum_customs "$@"
else
    exec "$@"
fi
