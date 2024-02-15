#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export PYTHONPATH="${PYTHONPATH}:${SCRIPT_DIR}"
conda develop "${SCRIPT_DIR}"