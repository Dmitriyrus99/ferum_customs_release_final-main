#!/bin/bash
set -e

# Execute bench setup with provided argument or default to dev
if [ $# -eq 0 ]; then
    exec /bench_setup.sh dev
else
    exec /bench_setup.sh "$@"
fi
