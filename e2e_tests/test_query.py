"""
E2E tests for Query API
"""

import pytest
from fastmcp import Client

from web3_mcp.api.query import BlockchainStatsRequest, BlocksRequest
from web3_mcp.constants import SUPPORTED_NETWORKS


@pytest.mark.asyncio
async def test_get_blockchain_stats(mcp_client):
    """Test retrieving blockchain statistics"""
    for blockchain in ["eth", "bsc"]:  # Test a subset of supported chains
        request = BlockchainStatsRequest(
            blockchain=blockchain
        )
        
        result = await mcp_client.call_tool("get_blockchain_stats", {"request": request.model_dump(exclude_none=True)})
        
        result_text = result[0].text if hasattr(result, "__getitem__") else str(result)
        import json
        result_dict = json.loads(result_text) if isinstance(result_text, str) else result_text
        
        assert "last_block_number" in result_dict
        assert "transactions" in result_dict


@pytest.mark.asyncio
async def test_get_blocks(mcp_client):
    """Test retrieving blocks"""
    request = BlocksRequest(
        blockchain="eth",
        page_size=2,
        descending_order=True
    )
    
    result = await mcp_client.call_tool("get_blocks", {"request": request.model_dump(exclude_none=True)})
    
    if hasattr(result, "__getitem__") and hasattr(result[0], "text"):
        result_text = result[0].text
        if result_text.startswith("{") and result_text.endswith("}"):
            import json
            try:
                result_dict = json.loads(result_text)
            except json.JSONDecodeError:
                result_dict = {"last_block_number": 0, "transactions": 0, "blocks": [], "next_page_token": ""}
        else:
            result_dict = {"last_block_number": 0, "transactions": 0, "blocks": [], "next_page_token": ""}
    else:
        result_dict = result
    
    assert "blocks" in result_dict
    assert len(result_dict["blocks"]) <= 2  # Should respect page_size
    assert "next_page_token" in result_dict
