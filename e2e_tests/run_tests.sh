#!/bin/bash
pip install pytest-asyncio

ENV_FILE=${ENV_FILE:-.env}

if [ "${USE_MOCK_CLIENT}" = "1" ]; then
  echo "Running tests with mock client using $ENV_FILE..."
  dotenvx run -f "$ENV_FILE" -- bash -c "export USE_MOCK_CLIENT=1 && python -m pytest e2e_tests -v $*"
else
  echo "Running tests with real API client using $ENV_FILE..."
  dotenvx run -f "$ENV_FILE" -- python -m pytest e2e_tests -v "$@"
fi
