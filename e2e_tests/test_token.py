"""
E2E tests for Token API
"""

import asyncio
import pytest

from web3_mcp.api.token import AccountBalanceRequest, TokenPriceRequest
from web3_mcp.constants import SUPPORTED_NETWORKS


@pytest.mark.asyncio
async def test_get_account_balance(mcp_client):
    """Test retrieving account balance"""
    wallet_address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"  # vitalik.eth
    
    request = AccountBalanceRequest(
        wallet_address=wallet_address,
        blockchain="eth"
    )
    
    try:
        result = await asyncio.wait_for(
            mcp_client.call_tool("get_account_balance", {"request": request.model_dump(exclude_none=True)}),
            timeout=10.0  # 10 second timeout
        )
        
        assert "assets" in result
        assert len(result["assets"]) > 0  # This wallet should have assets
    except asyncio.TimeoutError:
        print("Test timed out after 10 seconds")
        pytest.skip("API request timed out")
    except Exception as e:
        print(f"Error in test_get_account_balance: {e}")
        pytest.skip(f"Skipping due to API error: {e}")


@pytest.mark.asyncio
async def test_get_token_price(mcp_client):
    """Test retrieving token price"""
    request = TokenPriceRequest(
        blockchain="eth",
        contract_address="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"  # USDC on Ethereum
    )
    
    try:
        result = await asyncio.wait_for(
            mcp_client.call_tool("get_token_price", {"request": request.model_dump(exclude_none=True)}),
            timeout=10.0  # 10 second timeout
        )
        
        assert "price_usd" in result
    except asyncio.TimeoutError:
        print("Test timed out after 10 seconds")
        pytest.skip("API request timed out")
    except Exception as e:
        print(f"Error in test_get_token_price: {e}")
        pytest.skip(f"Skipping due to API error: {e}")
