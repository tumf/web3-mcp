#!/bin/bash
pip install pytest-asyncio
dotenvx run -f .env.devin -- python -m pytest e2e_tests -v "$@"
