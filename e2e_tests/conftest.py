"""
Test fixtures for e2e tests
"""

import asyncio
import os
import sys
from typing import Generator, AsyncGenerator

import pytest
import pytest_asyncio
from fastmcp import Client

from web3_mcp.auth import AnkrAuth
from web3_mcp.server import init_server

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
    """Initialize a client for making requests directly to the Ankr API"""
    endpoint, private_key = ankr_credentials
    
    # Create auth object with credentials
    auth = AnkrAuth(endpoint=endpoint, private_key=private_key)
    ankr_client = auth.client
    
    # Create a client that directly uses the API methods
    class DirectClient:
        def __init__(self, client):
            self.client = client
            
        async def call_tool(self, tool_name, params):
            request = params.get("request", {})
            
            if tool_name == "get_nfts_by_owner":
                from web3_mcp.api.nft import NFTByOwnerRequest, NFTApi
                request_obj = NFTByOwnerRequest(**request)
                api = NFTApi(self.client)
                result = await api.get_nfts_by_owner(request_obj)
                return result
            
            elif tool_name == "get_nft_metadata":
                from web3_mcp.api.nft import NFTMetadataRequest, NFTApi
                request_obj = NFTMetadataRequest(**request)
                api = NFTApi(self.client)
                result = await api.get_nft_metadata(request_obj)
                return result
            
            elif tool_name == "get_blockchain_stats":
                from web3_mcp.api.query import BlockchainStatsRequest, QueryApi
                request_obj = BlockchainStatsRequest(**request)
                api = QueryApi(self.client)
                result = await api.get_blockchain_stats(request_obj)
                return result
            
            elif tool_name == "get_blocks":
                from web3_mcp.api.query import BlocksRequest, QueryApi
                request_obj = BlocksRequest(**request)
                api = QueryApi(self.client)
                result = await api.get_blocks(request_obj)
                return result
            
            elif tool_name == "get_account_balance":
                from web3_mcp.api.token import AccountBalanceRequest, TokenApi
                request_obj = AccountBalanceRequest(**request)
                api = TokenApi(self.client)
                result = await api.get_account_balance(request_obj)
                return result
            
            elif tool_name == "get_token_price":
                from web3_mcp.api.token import TokenPriceRequest, TokenApi
                request_obj = TokenPriceRequest(**request)
                api = TokenApi(self.client)
                result = await api.get_token_price(request_obj)
                return result
            
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
    
    client = DirectClient(ankr_client)
    yield client
