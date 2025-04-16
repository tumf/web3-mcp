"""
E2E tests for Query API
"""

import pytest
from fastmcp import Client

from web3_mcp.api.query import BlockchainStatsRequest, BlocksRequest
from web3_mcp.constants import SUPPORTED_NETWORKS


@pytest.mark.asyncio
async def test_get_blockchain_stats(mcp_server):
    """Test retrieving blockchain statistics"""
    for blockchain in ["eth", "bsc"]:  # Test a subset of supported chains
        request = BlockchainStatsRequest(
            blockchain=blockchain
        )
        
        client = Client("http://127.0.0.1:8000")
        async with client:
            result = await client.call_tool("get_blockchain_stats", request.model_dump(exclude_none=True))
        
        assert "last_block_number" in result
        assert "transactions" in result


@pytest.mark.asyncio
async def test_get_blocks(mcp_server):
    """Test retrieving blocks"""
    request = BlocksRequest(
        blockchain="eth",
        page_size=2,
        descending_order=True
    )
    
    client = Client("http://127.0.0.1:8000")
    async with client:
        result = await client.call_tool("get_blocks", request.model_dump(exclude_none=True))
    
    assert "blocks" in result
    assert len(result["blocks"]) <= 2  # Should respect page_size
    assert "next_page_token" in result
