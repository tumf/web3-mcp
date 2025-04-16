#!/bin/bash
pip install pytest-asyncio

if [ "${USE_MOCK_CLIENT}" = "1" ]; then
  echo "Running tests with mock client..."
  dotenvx run -f .env.devin -- bash -c "export USE_MOCK_CLIENT=1 && python -m pytest e2e_tests -v $*"
else
  echo "Running tests with real API client..."
  dotenvx run -f .env.devin -- python -m pytest e2e_tests -v "$@"
fi
