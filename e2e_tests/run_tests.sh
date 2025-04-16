
pip install pytest-asyncio
dotenvx run -f .env.devin -- pytest e2e_tests -v "$@"
