"""
Test fixtures for e2e tests
"""

import asyncio
import os
import threading
from typing import Generator, AsyncGenerator
import time

import pytest
import pytest_asyncio
from fastmcp import Client

# from web3_mcp.server import init_server


def start_server_thread(mcp) -> threading.Thread:
    """Start the MCP server in a separate thread"""
    def run_server():
        import sys
        import os
        r_pipe, w_pipe = os.pipe()
        old_stdin, old_stdout = sys.stdin, sys.stdout
        
        r_file = os.fdopen(r_pipe, 'r')
        w_file = os.fdopen(w_pipe, 'w')
        
        sys.stdin = r_file
        sys.stdout = w_file
        
        try:
            mcp.run(transport="stdio")
        finally:
            sys.stdin, sys.stdout = old_stdin, old_stdout
            r_file.close()
            w_file.close()
        
    thread = threading.Thread(target=run_server)
    thread.daemon = True
    thread.start()
    time.sleep(2)  # Give the server time to start
    return thread


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for the test session"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def mcp_server() -> Generator[object, None, None]:
    """Initialize the MCP server for testing"""
    
    endpoint = os.environ.get("ANKR_ENDPOINT")
    private_key = os.environ.get("ANKR_PRIVATE_KEY", os.environ.get("DOTENV_PRIVATE_KEY_DEVIN"))
    
    if not endpoint or not private_key:
        pytest.skip("ANKR_ENDPOINT and ANKR_PRIVATE_KEY environment variables are required")
    
    from web3_mcp.server import init_server
    
    mcp = init_server(
        name="Ankr MCP Test",
        endpoint=endpoint,
        private_key=private_key,
    )
    
    server_thread = start_server_thread(mcp)
    
    print(f"Server initialized and started")
    
    yield mcp
    
    print("Server fixture cleanup complete")
    


@pytest_asyncio.fixture
async def mcp_client(mcp_server):
    """Initialize an MCP client for making requests to the server"""
    client = Client(transport=mcp_server)
    yield client
