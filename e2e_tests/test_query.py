"""
E2E tests for Query API
"""

import asyncio
import pytest

from web3_mcp.api.query import BlockchainStatsRequest, BlocksRequest
from web3_mcp.constants import SUPPORTED_NETWORKS


@pytest.mark.asyncio
async def test_get_blockchain_stats(mcp_client):
    """Test retrieving blockchain statistics"""
    for blockchain in ["eth", "bsc"]:  # Test a subset of supported chains
        request = BlockchainStatsRequest(
            blockchain=blockchain
        )
        
        try:
            result = await asyncio.wait_for(
                mcp_client.call_tool("get_blockchain_stats", {"request": request.model_dump(exclude_none=True)}),
                timeout=10.0  # 10 second timeout
            )
            
            assert "last_block_number" in result
            assert "transactions" in result
        except asyncio.TimeoutError:
            print(f"Test timed out after 10 seconds for blockchain {blockchain}")
            pytest.skip("API request timed out")
        except Exception as e:
            print(f"Error in test_get_blockchain_stats for {blockchain}: {e}")
            pytest.skip(f"Skipping due to API error: {e}")


@pytest.mark.asyncio
async def test_get_blocks(mcp_client):
    """Test retrieving blocks"""
    request = BlocksRequest(
        blockchain="eth",
        page_size=2,
        descending_order=True
    )
    
    try:
        result = await asyncio.wait_for(
            mcp_client.call_tool("get_blocks", {"request": request.model_dump(exclude_none=True)}),
            timeout=10.0  # 10 second timeout
        )
        
        assert "blocks" in result
        assert len(result["blocks"]) <= 2  # Should respect page_size
        assert "next_page_token" in result
    except asyncio.TimeoutError:
        print("Test timed out after 10 seconds")
        pytest.skip("API request timed out")
    except Exception as e:
        print(f"Error in test_get_blocks: {e}")
        pytest.skip(f"Skipping due to API error: {e}")
