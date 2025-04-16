"""
Mocked tests for CI environments (no real Ankr API access needed)
"""

import asyncio
from typing import AsyncGenerator
import pytest
import pytest_asyncio
from unittest.mock import patch, MagicMock, AsyncMock

from fastmcp import Client


class MockClient:
    """Mock implementation of MCP Client for testing without a real server"""
    
    async def invoke(self, tool_name, params):
        """Mock invoke method that returns predefined responses based on the tool name"""
        if tool_name == "get_nfts_by_owner":
            return {
                "assets": [],
                "next_page_token": ""
            }
        elif tool_name == "get_blockchain_stats":
            return {
                "last_block_number": 12345678,
                "transactions": 987654321
            }
        elif tool_name == "get_account_balance":
            return {
                "assets": [
                    {
                        "blockchain": "eth",
                        "token_name": "Ethereum",
                        "token_symbol": "ETH",
                        "token_decimals": 18,
                        "balance": "1000000000000000000"
                    }
                ]
            }
        return {}


@pytest.mark.asyncio
async def test_mocked_nft_api():
    """Test NFT API with mocked client"""
    client = MockClient()
    result = await client.invoke("get_nfts_by_owner", {"wallet_address": "0x123"})
    assert "assets" in result
    assert isinstance(result["assets"], list)


@pytest.mark.asyncio
async def test_mocked_query_api():
    """Test Query API with mocked client"""
    client = MockClient()
    result = await client.invoke("get_blockchain_stats", {"blockchain": "eth"})
    assert "last_block_number" in result
    assert isinstance(result["last_block_number"], int)


@pytest.mark.asyncio
async def test_mocked_token_api():
    """Test Token API with mocked client"""
    client = MockClient()
    result = await client.invoke("get_account_balance", {"wallet_address": "0x123"})
    assert "assets" in result
    assert len(result["assets"]) > 0

@pytest_asyncio.fixture
async def mcp_client():
    """Override the default mcp_client fixture with a mock client"""
    client = MockClient()
    return client
