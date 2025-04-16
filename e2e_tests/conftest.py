"""
Test fixtures for e2e tests
"""

import asyncio
import os
import sys
import threading
import time
from typing import Generator, AsyncGenerator

import pytest
import pytest_asyncio
from fastmcp import Client

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for the test session"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def ankr_credentials() -> tuple:
    """Get Ankr API credentials from environment variables"""
    endpoint = os.environ.get("ANKR_ENDPOINT")
    private_key = os.environ.get("ANKR_PRIVATE_KEY", os.environ.get("DOTENV_PRIVATE_KEY_DEVIN"))
    
    if not endpoint or not private_key:
        pytest.skip("ANKR_ENDPOINT and ANKR_PRIVATE_KEY environment variables are required")
    
    return endpoint, private_key

@pytest.fixture(scope="session")
def mcp_server(ankr_credentials) -> Generator[object, None, None]:
    """Initialize and run the MCP server for testing"""
    endpoint, private_key = ankr_credentials
    
    from web3_mcp.server import init_server
    
    # Initialize the server with the Ankr credentials
    mcp = init_server(
        name="Ankr MCP Test",
        endpoint=endpoint,
        private_key=private_key,
    )
    
    # Start the server in a thread
    def run_server():
        try:
            mcp.run(transport="stdio")
        except Exception as e:
            print(f"Server error: {e}")
    
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Give the server time to start
    time.sleep(1)
    
    print(f"Server initialized and started in thread")
    
    yield mcp
    
    print("Server fixture cleanup complete")

@pytest_asyncio.fixture
async def mcp_client(mcp_server):
    """Initialize an MCP client for making requests to the server"""
    # Create a client that connects to the server
    client = Client(transport=mcp_server)
    
    await client.open()
    
    yield client
    
    await client.close()
