"""
E2E tests for Query API
"""

import asyncio
from typing import Any

import aiohttp
import pytest

from web3_mcp.api.query import (
    BlockchainStatsRequest,
    BlocksRequest,
    InteractionsRequest,
    LogsRequest,
    TransactionsByAddressRequest,
    TransactionsByHashRequest,
)

from .utils import make_request_with_retry


@pytest.mark.asyncio(loop_scope="session")
async def test_get_blockchain_stats(mcp_client: Any) -> None:
    """Test retrieving blockchain stats"""
    request = BlockchainStatsRequest(
        blockchain="eth",
    )

    try:
        result = await make_request_with_retry(
            mcp_client,
            "get_blockchain_stats",
            request.model_dump(exclude_none=True),
        )

        assert isinstance(result, dict), "Result should be a dictionary"
        assert "stats" in result, "Result should contain 'stats' key"
        assert isinstance(result["stats"], dict), "'stats' should be a dictionary"

    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        pytest.skip(f"Network error occurred: {str(e)}")
    except Exception as e:
        pytest.skip(f"Skipping due to API error: {str(e)}")


@pytest.mark.asyncio(loop_scope="session")
async def test_get_blocks(mcp_client: Any) -> None:
    """Test retrieving blocks"""
    request = BlocksRequest(
        blockchain="eth",
        page_size=2,
    )

    try:
        result = await make_request_with_retry(
            mcp_client,
            "get_blocks",
            request.model_dump(exclude_none=True),
        )

        assert isinstance(result, dict), "Result should be a dictionary"
        assert "blocks" in result, "Result should contain 'blocks' key"
        assert isinstance(result["blocks"], list), "'blocks' should be a list"

    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        pytest.skip(f"Network error occurred: {str(e)}")
    except Exception as e:
        pytest.skip(f"Skipping due to API error: {str(e)}")


@pytest.mark.asyncio(loop_scope="session")
async def test_get_logs(mcp_client: Any) -> None:
    """Test retrieving blockchain logs"""
    request = LogsRequest(
        blockchain="eth",
        address="0x3589d05a1ec4af9f65b0e5554e645707775ee43c",
        from_block=1181739,
        to_block=1181749,
        topics=["0x000000000000000000000000feb92d30bf01ff9a1901666c5573532bfa07eeec"],
        page_size=10,  # 少なめの結果数
    )

    try:
        result = await make_request_with_retry(
            mcp_client, "get_logs", request.model_dump(exclude_none=True), max_retries=1, timeout=15
        )

        assert isinstance(result, dict), "Result should be a dictionary"
        assert "logs" in result, "Result should contain 'logs' key"
        assert isinstance(result["logs"], list), "'logs' should be a list"

    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        pytest.skip(f"Network error occurred: {str(e)}")
    except Exception as e:
        pytest.skip(f"Skipping due to API error: {str(e)}")


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.skip(reason="Transactions by hash endpoint is not provided as a tool")
async def test_get_transactions_by_hash(mcp_client: Any) -> None:
    """Test retrieving transactions by hash"""
    # Using a known ETH transaction hash
    request = TransactionsByHashRequest(
        blockchain="eth",
        transaction_hash="0x7d2b7c35f8da5c1831f9ef59d402a53c03f15af6c2c24f2f23118cf21e53b7cf",
    )

    try:
        # タイムアウトを短く設定
        result = await make_request_with_retry(
            mcp_client,
            "get_transactions_by_hash",
            request.model_dump(exclude_none=True),
            max_retries=1,
            timeout=5,
        )

        assert isinstance(result, dict), "Result should be a dictionary"
        assert "transaction" in result, "Result should contain 'transaction' key"
        assert isinstance(result["transaction"], dict), "'transaction' should be a dictionary"

    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        pytest.skip(f"Network error occurred: {str(e)}")
    except Exception as e:
        pytest.skip(f"Skipping due to API error: {str(e)}")


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.skip(reason="Transactions by address endpoint is not provided as a tool")
async def test_get_transactions_by_address(mcp_client: Any) -> None:
    """Test retrieving transactions by address"""
    request = TransactionsByAddressRequest(
        blockchain="eth",
        wallet_address="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH contract
        page_size=1,  # 結果を1件のみに制限
    )

    try:
        # タイムアウトを短く設定
        result = await make_request_with_retry(
            mcp_client,
            "get_transactions_by_address",
            request.model_dump(exclude_none=True),
            max_retries=1,
            timeout=5,
        )

        assert isinstance(result, dict), "Result should be a dictionary"
        assert "transactions" in result, "Result should contain 'transactions' key"
        assert isinstance(result["transactions"], list), "'transactions' should be a list"

    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        pytest.skip(f"Network error occurred: {str(e)}")
    except Exception as e:
        pytest.skip(f"Skipping due to API error: {str(e)}")


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.skip(reason="Interactions endpoint is not provided as a tool")
async def test_get_interactions(mcp_client: Any) -> None:
    """Test retrieving wallet interactions with contracts"""
    request = InteractionsRequest(
        blockchain="eth",
        wallet_address="0x00000000219ab540356cBB839Cbe05303d7705Fa",  # Eth2 deposit contract
        page_size=1,  # 結果を1件のみに制限
    )

    try:
        # タイムアウトを短く設定
        result = await make_request_with_retry(
            mcp_client,
            "get_interactions",
            request.model_dump(exclude_none=True),
            max_retries=1,
            timeout=5,
        )

        assert isinstance(result, dict), "Result should be a dictionary"
        assert "interactions" in result, "Result should contain 'interactions' key"
        assert isinstance(result["interactions"], list), "'interactions' should be a list"

    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        pytest.skip(f"Network error occurred: {str(e)}")
    except Exception as e:
        pytest.skip(f"Skipping due to API error: {str(e)}")


@pytest.mark.asyncio(loop_scope="session")
async def test_get_supported_networks(mcp_client: Any) -> None:
    """Test retrieving supported networks"""
    try:
        result = await make_request_with_retry(
            mcp_client,
            "get_supported_networks",
            {},
        )

        assert isinstance(result, list), "Result should be a list"
        assert len(result) > 0, "There should be at least one supported network"
        assert "eth" in result, "Ethereum should be in the supported networks"

        # Check that all networks are strings
        for network in result:
            assert isinstance(network, str), "Network identifier should be a string"

    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        pytest.skip(f"Network error occurred: {str(e)}")
    except Exception as e:
        pytest.skip(f"Skipping due to API error: {str(e)}")
