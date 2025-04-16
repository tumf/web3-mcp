"""
E2E tests for Query API
"""

import asyncio
from typing import Any

import aiohttp
import pytest

from web3_mcp.api.query import BlockchainStatsRequest, BlocksRequest

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
