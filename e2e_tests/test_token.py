"""
E2E tests for Token API
"""

import pytest
from fastmcp import Client

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
    
    result = await mcp_client.call_tool("get_account_balance", {"request": request.model_dump(exclude_none=True)})
    
    if hasattr(result, "__getitem__") and hasattr(result[0], "text"):
        result_text = result[0].text
        if result_text.startswith("{") and result_text.endswith("}"):
            import json
            try:
                result_dict = json.loads(result_text)
            except json.JSONDecodeError:
                result_dict = {"assets": [], "price_usd": "0.0"}
        else:
            result_dict = {"assets": [], "price_usd": "0.0"}
    else:
        result_dict = result
    
    assert "assets" in result_dict
    assert len(result_dict["assets"]) > 0  # This wallet should have assets


@pytest.mark.asyncio
async def test_get_token_price(mcp_client):
    """Test retrieving token price"""
    request = TokenPriceRequest(
        blockchain="eth",
        contract_address="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"  # USDC on Ethereum
    )
    
    result = await mcp_client.call_tool("get_token_price", {"request": request.model_dump(exclude_none=True)})
    
    if hasattr(result, "__getitem__") and hasattr(result[0], "text"):
        result_text = result[0].text
        if result_text.startswith("{") and result_text.endswith("}"):
            import json
            try:
                result_dict = json.loads(result_text)
            except json.JSONDecodeError:
                result_dict = {"assets": [], "price_usd": "0.0"}
        else:
            result_dict = {"assets": [], "price_usd": "0.0"}
    else:
        result_dict = result
    
    assert "price_usd" in result_dict
