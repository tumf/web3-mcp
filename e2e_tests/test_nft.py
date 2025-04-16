"""
E2E tests for NFT API
"""

import pytest
from fastmcp import Client

from web3_mcp.api.nft import NFTByOwnerRequest, NFTMetadataRequest
from web3_mcp.constants import SUPPORTED_NETWORKS


@pytest.mark.asyncio
async def test_get_nfts_by_owner(mcp_client):
    """Test retrieving NFTs by owner"""
    wallet_address = "0x19818f44faf5a217f619aff0fd487cb2a55cca65"  # Example wallet
    
    request = NFTByOwnerRequest(
        wallet_address=wallet_address,
        blockchain="eth",
        page_size=2
    )
    
    result = await mcp_client.invoke("get_nfts_by_owner", request.model_dump(exclude_none=True))
    
    assert "assets" in result
    assert "next_page_token" in result


@pytest.mark.asyncio
async def test_get_nft_metadata(mcp_client):
    """Test retrieving NFT metadata"""
    request = NFTMetadataRequest(
        blockchain="eth",
        contract_address="0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB",
        token_id="7804"
    )
    
    result = await mcp_client.invoke("get_nft_metadata", request.model_dump(exclude_none=True))
    
    assert "name" in result
    assert "image" in result or "image_url" in result
