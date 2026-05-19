#!/bin/bash
set -e

# This script helps ensure the harness run directory exists for idea-refine outputs.

RUNS_DIR="harness/runs"

if [ ! -d "$RUNS_DIR" ]; then
  mkdir -p "$RUNS_DIR"
  echo "Created directory: $RUNS_DIR" >&2
else
  echo "Directory already exists: $RUNS_DIR" >&2
fi

echo "{\"status\": \"ready\", \"directory\": \"$RUNS_DIR\"}"
