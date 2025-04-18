"""
E2E tests for Token API
"""

import asyncio
from enum import Enum
from typing import Any, Dict, List

import aiohttp
import pytest

from web3_mcp.api.token import TokenHoldersRequest  # Available but not provided as a tool
from web3_mcp.api.token import (
    AccountBalanceRequest,
    CurrenciesRequest,
    TokenHoldersCountRequest,
    TokenPriceRequest,
    TokenTransfersRequest,
)

from .utils import make_request_with_retry


def has_attributes(obj: Dict[str, Any], attributes: List[str]) -> bool:
    """Check if a dictionary has all the specified keys"""
    return all(attr in obj for attr in attributes)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_account_balance(mcp_client: Any) -> None:
    """Test retrieving account balance"""
    # Using a wallet with known token balance
    wallet_address = "0x47ac0fb4f2d84898e4d9e7b4dab3c24507a6d503"  # Binance's wallet

    request = AccountBalanceRequest(
        wallet_address=wallet_address,
        blockchain="eth",
    )

    try:
        result = await make_request_with_retry(
            mcp_client,
            "get_account_balance",
            request.model_dump(exclude_none=True),
        )

        assert isinstance(result, dict), "Result should be a dictionary"
        assert "assets" in result, "Result should contain 'assets' key"
        assert isinstance(result["assets"], list), "'assets' should be a list"

        if len(result["assets"]) > 0:
            asset = result["assets"][0]
            required_fields = [
                "balance",
                "balanceRawInteger",
                "balanceUsd",
                "blockchain",
                "holderAddress",
                "thumbnail",
                "tokenDecimals",
                "tokenName",
                "tokenPrice",
                "tokenSymbol",
                "tokenType",
            ]
            assert has_attributes(
                asset, required_fields
            ), f"Asset should have all required attributes: {required_fields}"

            assert isinstance(asset["tokenDecimals"], int), "tokenDecimals should be an integer"
            assert isinstance(asset["balance"], str), "balance should be a string"
            assert isinstance(asset["tokenSymbol"], str), "tokenSymbol should be a string"

            # Check blockchain field
            blockchain = asset["blockchain"]
            assert isinstance(blockchain, Enum), "blockchain should be an Enum"
            assert str(blockchain.value) == "eth", "blockchain value should be 'eth'"

    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        pytest.skip(f"Network error occurred: {str(e)}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {str(e)}")


@pytest.mark.asyncio(loop_scope="session")
async def test_get_token_price(mcp_client: Any) -> None:
    """Test retrieving token price"""
    request = TokenPriceRequest(
        blockchain="eth",
        contract_address="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC on Ethereum
    )

    try:
        result = await make_request_with_retry(
            mcp_client,
            "get_token_price",
            request.model_dump(exclude_none=True),
        )

        assert isinstance(result, dict), "Result should be a dictionary"
        assert "price_usd" in result, "Result should contain 'price_usd' key"
        assert isinstance(result["price_usd"], str), "price_usd should be a string"

        # Convert price_usd to float for value check
        price_usd = float(result["price_usd"])
        assert price_usd > 0, "price_usd should be positive"

    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        pytest.skip(f"Network error occurred: {str(e)}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {str(e)}")


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.skip(reason="Currencies endpoint is not provided as a tool")
async def test_get_currencies(mcp_client: Any) -> None:
    """Test retrieving available currencies"""
    request = CurrenciesRequest()

    try:
        result = await make_request_with_retry(
            mcp_client,
            "get_currencies",
            request.model_dump(exclude_none=True),
            max_retries=1,
            timeout=15,
        )

        assert isinstance(result, dict), "Result should be a dictionary"
        assert "currencies" in result, "Result should contain 'currencies' key"
        assert isinstance(result["currencies"], list), "'currencies' should be a list"

        if len(result["currencies"]) > 0:
            currency = result["currencies"][0]
            required_fields = ["symbol", "name", "decimals"]
            assert has_attributes(
                currency, required_fields
            ), f"Currency should have all required attributes: {required_fields}"

    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        pytest.skip(f"Network error occurred: {str(e)}")
    except Exception as e:
        pytest.skip(f"Skipping due to API error: {str(e)}")


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.skip(reason="Token Holders endpoint is not provided as a tool")
async def test_get_token_holders(mcp_client: Any) -> None:
    """Test retrieving token holders"""
    request = TokenHoldersRequest(
        blockchain="eth",
        contract_address="0xdac17f958d2ee523a2206206994597c13d831ec7",  # Tether (USDT)
        page_size=5,  # Small amount of data
    )

    try:
        result = await make_request_with_retry(
            mcp_client,
            "get_token_holders",
            request.model_dump(exclude_none=True),
            max_retries=1,
            timeout=15,
        )

        assert isinstance(result, dict), "Result should be a dictionary"
        assert "holders" in result, "Result should contain 'holders' key"
        assert isinstance(result["holders"], list), "'holders' should be a list"
        assert "next_page_token" in result, "Result should contain 'next_page_token' key"

    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        pytest.skip(f"Network error occurred: {str(e)}")
    except Exception as e:
        pytest.skip(f"Skipping due to API error: {str(e)}")


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.skip(reason="Token Holders Count endpoint is not provided as a tool")
async def test_get_token_holders_count(mcp_client: Any) -> None:
    """Test retrieving token holders count"""
    request = TokenHoldersCountRequest(
        blockchain="eth",
        contract_address="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC on Ethereum
    )

    try:
        result = await make_request_with_retry(
            mcp_client,
            "get_token_holders_count",
            request.model_dump(exclude_none=True),
        )

        assert isinstance(result, dict), "Result should be a dictionary"
        assert "count" in result, "Result should contain 'count' key"
        assert isinstance(result["count"], int), "'count' should be an integer"
        assert result["count"] > 0, "Token holder count should be greater than 0"

    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        pytest.skip(f"Network error occurred: {str(e)}")
    except Exception as e:
        pytest.skip(f"Skipping due to API error: {str(e)}")


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.skip(reason="Token Transfers endpoint is not provided as a tool")
async def test_get_token_transfers(mcp_client: Any) -> None:
    """Test retrieving token transfers"""
    request = TokenTransfersRequest(
        blockchain="eth",
        contract_address="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC on Ethereum
        page_size=1,
    )

    try:
        result = await make_request_with_retry(
            mcp_client,
            "get_token_transfers",
            request.model_dump(exclude_none=True),
            max_retries=1,
            timeout=5,
        )

        assert isinstance(result, dict), "Result should be a dictionary"
        assert "transfers" in result, "Result should contain 'transfers' key"
        assert isinstance(result["transfers"], list), "'transfers' should be a list"
        assert "next_page_token" in result, "Result should contain 'next_page_token' key"

    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        pytest.skip(f"Network error occurred: {str(e)}")
    except Exception as e:
        pytest.skip(f"Skipping due to API error: {str(e)}")
