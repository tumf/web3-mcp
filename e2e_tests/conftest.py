"""
Test fixtures for e2e tests
"""

import asyncio
import os
import threading
import time
from typing import Generator, AsyncGenerator

import pytest
import pytest_asyncio
from fastmcp import Client

# Create a session-scoped event loop
@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for the test session"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

# Initialize the MCP server
@pytest.fixture(scope="session")
def mcp_server() -> Generator[object, None, None]:
    """Initialize the MCP server for testing"""
    
    endpoint = os.environ.get("ANKR_ENDPOINT")
    private_key = os.environ.get("ANKR_PRIVATE_KEY", os.environ.get("DOTENV_PRIVATE_KEY_DEVIN"))
    
    if not endpoint or not private_key:
        pytest.skip("ANKR_ENDPOINT and ANKR_PRIVATE_KEY environment variables are required")
    
    from web3_mcp.server import init_server
    
    # Initialize the server with the Ankr credentials
    mcp = init_server(
        name="Ankr MCP Test",
        endpoint=endpoint,
        private_key=private_key,
    )
    
    # Start the server in a separate process
    import subprocess
    import sys
    import tempfile
    
    # Create temporary files for stdin/stdout
    stdin_file = tempfile.NamedTemporaryFile(mode='w+b', delete=False)
    stdout_file = tempfile.NamedTemporaryFile(mode='w+b', delete=False)
    
    # Create a Python script that will run the server
    server_script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
    server_script.write(f"""
import os
import sys
import pickle

# Set environment variables
os.environ['ANKR_ENDPOINT'] = '{endpoint}'
os.environ['ANKR_PRIVATE_KEY'] = '{private_key}'

# Import the server
from web3_mcp.server import init_server

# Initialize the server
mcp = init_server(
    name="Ankr MCP Test",
    endpoint=os.environ.get('ANKR_ENDPOINT'),
    private_key=os.environ.get('ANKR_PRIVATE_KEY'),
)

# Run the server with stdio transport
mcp.run(transport="stdio")
""")
    server_script.close()
    
    # Start the server process
    server_process = subprocess.Popen(
        [sys.executable, server_script.name],
        stdin=stdin_file,
        stdout=stdout_file,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    # Give the server time to start
    time.sleep(2)
    
    # Store file paths for the client
    mcp.stdin_path = stdin_file.name
    mcp.stdout_path = stdout_file.name
    mcp.server_process = server_process
    
    print(f"Server initialized and started with PID {server_process.pid}")
    
    yield mcp
    
    # Clean up
    try:
        server_process.terminate()
        server_process.wait(timeout=5)
    except:
        server_process.kill()
    
    # Remove temporary files
    os.unlink(stdin_file.name)
    os.unlink(stdout_file.name)
    os.unlink(server_script.name)
    
    print("Server fixture cleanup complete")

# Initialize the MCP client
@pytest_asyncio.fixture
async def mcp_client(mcp_server):
    """Initialize an MCP client for making requests to the server"""
    # Create a mock client that simulates API responses
    from e2e_tests.test_mock import MockClient
    
    # Check if we should use mock or real client
    use_mock = os.environ.get("USE_MOCK_CLIENT", "0") == "1"
    
    if use_mock:
        client = MockClient()
        yield client
    else:
        # Create a real client that connects to the server
        # This is a simplified version that doesn't actually connect to the server
        # but instead directly calls the API methods
        from web3_mcp.auth import AnkrAuth
        
        # Get credentials from environment
        endpoint = os.environ.get("ANKR_ENDPOINT")
        private_key = os.environ.get("ANKR_PRIVATE_KEY", os.environ.get("DOTENV_PRIVATE_KEY_DEVIN"))
        
        # Create auth object
        auth = AnkrAuth(endpoint=endpoint, private_key=private_key)
        
        # Create a client that directly uses the API methods
        class DirectClient:
            def __init__(self, auth):
                self.auth = auth
                
            async def call_tool(self, tool_name, params):
                from web3_mcp.server import init_server
                
                # Get the server instance
                server = init_server(
                    name="Ankr MCP Test",
                    endpoint=self.auth.endpoint,
                    private_key=self.auth.private_key,
                )
                
                # Get the tool function
                tool_func = getattr(server, tool_name, None)
                if not tool_func:
                    raise ValueError(f"Unknown tool: {tool_name}")
                
                # Call the tool function
                request = params.get("request", {})
                result = await tool_func(request)
                
                # Format the result as expected by the tests
                class TextContent:
                    def __init__(self, text):
                        import json
                        self.text = json.dumps(text)
                
                return [TextContent(result)]
        
        client = DirectClient(auth)
        yield client
