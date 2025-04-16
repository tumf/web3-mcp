pip install pytest-asyncio

ENV_FILE=${ENV_FILE:-.env}

echo "Running mock tests using $ENV_FILE..."
dotenvx run -f "$ENV_FILE" -- python -m pytest e2e_tests/test_mock.py -v "$@"
