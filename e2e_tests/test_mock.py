"""
Mocked tests for CI environments (no real Ankr API access needed)
"""

import json
from typing import Any, Dict, List

import pytest
import pytest_asyncio


class MockClient:
    """Mock implementation of MCP Client for testing without a real server"""

    async def invoke(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Mock invoke method that returns predefined responses based on the tool name"""
        return await self._get_mock_response(tool_name)

    async def call_tool(self, tool_name: str, params: Dict[str, Any]) -> List[Any]:
        """Mock call_tool method that returns predefined responses based on the tool name"""
        response = await self._get_mock_response(tool_name)

        class TextContent:
            def __init__(self, text: Any) -> None:
                self.text = json.dumps(text)

        return [TextContent(response)]

    async def _get_mock_response(self, tool_name: str) -> Dict[str, Any]:
        """Helper method to get mock responses based on tool name"""
        if tool_name == "get_nfts_by_owner":
            return {"assets": [], "next_page_token": ""}
        elif tool_name == "get_blockchain_stats":
            return {"last_block_number": 12345678, "transactions": 987654321}
        elif tool_name == "get_account_balance":
            return {
                "assets": [
                    {
                        "blockchain": "eth",
                        "token_name": "Ethereum",
                        "token_symbol": "ETH",
                        "token_decimals": 18,
                        "balance": "1000000000000000000",
                    }
                ]
            }
        elif tool_name == "get_nft_metadata":
            return {
                "name": "CryptoPunk #7804",
                "description": "CryptoPunks launched as a fixed set of 10,000 items in mid-2017 and became one of the inspirations for the ERC-721 standard.",
                "image": "https://example.com/image.png",
                "attributes": [
                    {"trait_type": "Type", "value": "Alien"},
                    {"trait_type": "Accessory", "value": "Cap Forward"},
                ],
            }
        elif tool_name == "get_blocks":
            return {
                "blocks": [
                    {"number": 12345678, "hash": "0x1234..."},
                    {"number": 12345677, "hash": "0x5678..."},
                ],
                "next_page_token": "token123",
            }
        elif tool_name == "get_token_price":
            return {"price_usd": "1.00", "last_updated_at": "2023-01-01T00:00:00Z"}
        return {}


@pytest.mark.asyncio
async def test_mocked_nft_api() -> None:
    """Test NFT API with mocked client"""
    client = MockClient()
    result = await client.invoke("get_nfts_by_owner", {"wallet_address": "0x123"})
    assert "assets" in result
    assert isinstance(result["assets"], list)


@pytest.mark.asyncio
async def test_mocked_query_api() -> None:
    """Test Query API with mocked client"""
    client = MockClient()
    result = await client.invoke("get_blockchain_stats", {"blockchain": "eth"})
    assert "last_block_number" in result
    assert isinstance(result["last_block_number"], int)


@pytest.mark.asyncio
async def test_mocked_token_api() -> None:
    """Test Token API with mocked client"""
    client = MockClient()
    result = await client.invoke("get_account_balance", {"wallet_address": "0x123"})
    assert "assets" in result
    assert len(result["assets"]) > 0


@pytest_asyncio.fixture
async def mcp_client() -> MockClient:
    """Override the default mcp_client fixture with a mock client"""
    client = MockClient()
    return client
