"""
E2E tests for Token API
"""

import pytest
from fastmcp import Client

from web3_mcp.api.token import AccountBalanceRequest, TokenPriceRequest
from web3_mcp.constants import SUPPORTED_NETWORKS


@pytest.mark.asyncio
async def test_get_account_balance(mcp_server):
    """Test retrieving account balance"""
    wallet_address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"  # vitalik.eth
    
    request = AccountBalanceRequest(
        wallet_address=wallet_address,
        blockchain="eth"
    )
    
    client = Client("http://127.0.0.1:8000")
    async with client:
        result = await client.call_tool("get_account_balance", request.model_dump(exclude_none=True))
    
    assert "assets" in result
    assert len(result["assets"]) > 0  # This wallet should have assets


@pytest.mark.asyncio
async def test_get_token_price(mcp_server):
    """Test retrieving token price"""
    request = TokenPriceRequest(
        blockchain="eth",
        contract_address="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"  # USDC on Ethereum
    )
    
    client = Client("http://127.0.0.1:8000")
    async with client:
        result = await client.call_tool("get_token_price", request.model_dump(exclude_none=True))
    
    assert "price_usd" in result
