"""
Test fixtures for e2e tests
"""

import asyncio
import os
import sys
import threading
from typing import Generator, AsyncGenerator
import time

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

@pytest_asyncio.fixture
async def mcp_client(ankr_credentials):
    """Initialize a direct client for making requests to the Ankr API"""
    from ankr import AnkrWeb3
    from web3_mcp.auth import AnkrAuth
    
    endpoint, private_key = ankr_credentials
    
    # Create a direct connection to the Ankr API using the same method as in auth.py
    auth = AnkrAuth(endpoint=endpoint, private_key=private_key)
    ankr_client = auth.client
    
    # Create a custom client that directly calls the API methods
    class DirectClient:
        def __init__(self, client):
            self.client = client
            
        async def call_tool(self, tool_name, params):
            request = params.get("request", {})
            
            # Map tool names to API methods
            if tool_name == "get_nfts_by_owner":
                from web3_mcp.api.nft import NFTByOwnerRequest, NFTApi
                request_obj = NFTByOwnerRequest(**request)
                api = NFTApi(self.client)
                result = await api.get_nfts_by_owner(request_obj)
            
            elif tool_name == "get_nft_metadata":
                from web3_mcp.api.nft import NFTMetadataRequest, NFTApi
                request_obj = NFTMetadataRequest(**request)
                api = NFTApi(self.client)
                result = await api.get_nft_metadata(request_obj)
            
            elif tool_name == "get_blockchain_stats":
                from web3_mcp.api.query import BlockchainStatsRequest, QueryApi
                request_obj = BlockchainStatsRequest(**request)
                api = QueryApi(self.client)
                result = await api.get_blockchain_stats(request_obj)
            
            elif tool_name == "get_blocks":
                from web3_mcp.api.query import BlocksRequest, QueryApi
                request_obj = BlocksRequest(**request)
                api = QueryApi(self.client)
                result = await api.get_blocks(request_obj)
            
            elif tool_name == "get_account_balance":
                from web3_mcp.api.token import AccountBalanceRequest, TokenApi
                request_obj = AccountBalanceRequest(**request)
                api = TokenApi(self.client)
                result = await api.get_account_balance(request_obj)
            
            elif tool_name == "get_token_price":
                from web3_mcp.api.token import TokenPriceRequest, TokenApi
                request_obj = TokenPriceRequest(**request)
                api = TokenApi(self.client)
                result = await api.get_token_price(request_obj)
            
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
            
            # Format the result as expected by the tests
            class TextContent:
                def __init__(self, text):
                    import json
                    self.text = json.dumps(text)
            
            return [TextContent(result)]
    
    client = DirectClient(ankr_client)
    yield client
