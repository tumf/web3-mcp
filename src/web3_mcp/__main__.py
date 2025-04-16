"""
Entry point for running MCP server
"""

import os
import sys

from .server import init_server


def main() -> None:
    """Run MCP server"""
    endpoint = os.environ.get("ANKR_ENDPOINT")
    private_key = os.environ.get("ANKR_PRIVATE_KEY", os.environ.get("DOTENV_PRIVATE_KEY_DEVIN"))

    if not endpoint:
        print("Error: ANKR_ENDPOINT environment variable is not set", file=sys.stderr)
        sys.exit(1)

    if not private_key:
        print("Warning: ANKR_PRIVATE_KEY environment variable is not set", file=sys.stderr)
        print("Some API calls may fail without authentication", file=sys.stderr)

    mcp = init_server(
        name="Ankr MCP",
        endpoint=endpoint,
        private_key=private_key,
    )
    mcp.run()


if __name__ == "__main__":
    main()
