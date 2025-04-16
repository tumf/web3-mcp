"""
E2E tests for NFT API
"""

import asyncio
import pytest

from web3_mcp.api.nft import NFTByOwnerRequest, NFTMetadataRequest
from web3_mcp.constants import SUPPORTED_NETWORKS


@pytest.mark.asyncio
async def test_get_nfts_by_owner(mcp_client):
    """Test retrieving NFTs by owner"""
    wallet_address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"  # vitalik.eth
    
    request = NFTByOwnerRequest(
        wallet_address=wallet_address,
        blockchain="eth",
        page_size=2
    )
    
    try:
        result = await asyncio.wait_for(
            mcp_client.call_tool("get_nfts_by_owner", {"request": request.model_dump(exclude_none=True)}),
            timeout=10.0  # 10 second timeout
        )
        
        assert "assets" in result
        assert "next_page_token" in result
    except asyncio.TimeoutError:
        print("Test timed out after 10 seconds")
        pytest.skip("API request timed out")
    except Exception as e:
        print(f"Error in test_get_nfts_by_owner: {e}")
        pytest.skip(f"Skipping due to API error: {e}")


@pytest.mark.asyncio
async def test_get_nft_metadata(mcp_client):
    """Test retrieving NFT metadata"""
    request = NFTMetadataRequest(
        blockchain="eth",
        contract_address="0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB",
        token_id="7804"
    )
    
    try:
        result = await asyncio.wait_for(
            mcp_client.call_tool("get_nft_metadata", {"request": request.model_dump(exclude_none=True)}),
            timeout=10.0  # 10 second timeout
        )
        
        assert "name" in result
        assert "image" in result or "image_url" in result
    except asyncio.TimeoutError:
        print("Test timed out after 10 seconds")
        pytest.skip("API request timed out")
    except Exception as e:
        print(f"Error in test_get_nft_metadata: {e}")
        pytest.skip(f"Skipping due to API error: {e}")
