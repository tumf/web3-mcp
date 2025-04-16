"""
Simple example of running the FactMCP server
"""

import os
from web3_mcp.server import FactMCP

endpoint = os.environ.get("ANKR_ENDPOINT")
private_key = os.environ.get("ANKR_PRIVATE_KEY", 
                             os.environ.get("DOTENV_PRIVATE_KEY_DEVIN"))

if not endpoint:
    raise ValueError("ANKR_ENDPOINT environment variable is not set")

server = FactMCP(
    name="Ankr FactMCP Example",
    endpoint=endpoint,
    private_key=private_key,
)

if __name__ == "__main__":
    server.run()
