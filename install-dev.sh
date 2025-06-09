#!/bin/bash
set -e

# create Python virtual environment if not exists
if [ ! -d .venv ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install -U pip
pip install -r dev-requirements.txt
