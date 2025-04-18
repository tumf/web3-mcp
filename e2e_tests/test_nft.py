"""
E2E tests for NFT API
"""

import asyncio
from typing import Any

import aiohttp
import pytest
from ankr.types import NftMetadata, SyncStatus

from web3_mcp.api.nft import (
    NFTByOwnerRequest,
    NFTHoldersRequest,
    NFTMetadataRequest,
    NFTTransfersRequest,
)

from .utils import make_request_with_retry


@pytest.mark.asyncio(loop_scope="session")
async def test_get_nfts_by_owner(mcp_client: Any) -> None:
    """Test retrieving NFTs by owner"""
    # Using a wallet with fewer NFTs for testing
    wallet_address = "0x1234567890123456789012345678901234567890"

    request = NFTByOwnerRequest(
        wallet_address=wallet_address,
        blockchain="eth",
        page_size=2,
    )

    try:
        result = await make_request_with_retry(
            mcp_client,
            "get_nfts_by_owner",
            request.model_dump(exclude_none=True),
        )

        assert isinstance(result, dict), "Result should be a dictionary"
        assert "assets" in result, "Result should contain 'assets' key"
        assert isinstance(result["assets"], list), "'assets' should be a list"

    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        pytest.skip(f"Network error occurred: {str(e)}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {str(e)}")


@pytest.mark.asyncio(loop_scope="session")
async def test_get_nft_metadata(mcp_client: Any) -> None:
    """Test retrieving NFT metadata"""
    request = NFTMetadataRequest(
        blockchain="eth",
        contract_address="0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB",  # CryptoPunks
        token_id="7804",
    )

    try:
        result = await make_request_with_retry(
            mcp_client,
            "get_nft_metadata",
            request.model_dump(exclude_none=True),
        )

        assert isinstance(result, dict), "Result should be a dictionary"
        assert "metadata" in result, "Result should contain 'metadata' key"
        assert isinstance(
            result["metadata"], NftMetadata
        ), "metadata should be an NftMetadata object"
        assert "syncStatus" in result, "Result should contain 'syncStatus' key"
        assert isinstance(
            result["syncStatus"], SyncStatus
        ), "syncStatus should be a SyncStatus object"

    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        pytest.skip(f"Network error occurred: {str(e)}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {str(e)}")


@pytest.mark.asyncio(loop_scope="session")
async def test_get_nft_holders(mcp_client: Any) -> None:
    """Test retrieving NFT holders"""
    request = NFTHoldersRequest(
        blockchain="eth",
        contract_address="0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB",  # CryptoPunks
        page_size=2,
    )

    try:
        result = await make_request_with_retry(
            mcp_client,
            "get_nft_holders",
            request.model_dump(exclude_none=True),
        )

        assert isinstance(result, dict), "Result should be a dictionary"
        assert "holders" in result, "Result should contain 'holders' key"
        assert isinstance(result["holders"], list), "'holders' should be a list"
        assert "next_page_token" in result, "Result should contain 'next_page_token' key"

    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        pytest.skip(f"Network error occurred: {str(e)}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {str(e)}")


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.skip(reason="NFT Transfers endpoint is not provided as a tool")
async def test_get_nft_transfers(mcp_client: Any) -> None:
    """Test retrieving NFT transfers"""
    request = NFTTransfersRequest(
        blockchain="eth",
        contract_address="0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB",  # CryptoPunks
        page_size=1,  # 結果を1件のみに制限
    )

    try:
        # タイムアウトを短く設定
        result = await make_request_with_retry(
            mcp_client,
            "get_nft_transfers",
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
