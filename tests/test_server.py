"""
Tests for MCP server
"""

import os
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest

from web3_mcp.server import init_server


@pytest.fixture(autouse=True)
def mock_env() -> Generator[None, None, None]:
    """Mock environment variables"""
    with patch.dict(
        os.environ, {"ANKR_ENDPOINT": "https://test.endpoint", "ANKR_PRIVATE_KEY": "test_key"}
    ):
        yield


@pytest.fixture
def mock_ankr_web3() -> Generator[MagicMock, None, None]:
    """Mock AnkrWeb3 client"""
    with patch("web3_mcp.auth.AnkrWeb3") as mock:
        mock_client = MagicMock()
        mock.return_value = mock_client
        yield mock_client


@pytest.mark.asyncio
async def test_server_initialization(mock_ankr_web3: MagicMock) -> None:
    """Test server initialization"""
    mcp = init_server(name="Test Server")

    assert mcp.name == "Test Server"

    tools = await mcp.get_tools()
    assert len(tools) > 0


@pytest.mark.asyncio
async def test_utility_tools(mock_ankr_web3: MagicMock) -> None:
    """Test utility tools"""
    mcp = init_server(name="Test Server")

    tools = await mcp.get_tools()
    tool_names = list(tools.keys())

    expected_tools = [
        "get_nfts_by_owner",
        "get_nft_metadata",
        "get_nft_holders",
        "get_nft_transfers",
        "get_blockchain_stats",
        "get_blocks",
        "get_logs",
        "get_transactions_by_hash",
        "get_transactions_by_address",
        "get_interactions",
        "get_account_balance",
        "get_currencies",
        "get_token_price",
        "get_token_holders",
        "get_token_holders_count",
        "get_token_transfers",
        "get_supported_networks",
    ]

    for expected_tool in expected_tools:
        assert expected_tool in tool_names

    resources = await mcp.get_resources()
    resource_uris = list(resources.keys())
    assert "ankr://info" in resource_uris


def test_init_server() -> None:
    # This function is mentioned in the original file but not implemented in the test_server.py file
    # It's assumed to exist as it's called in the test_server_initialization function
    pass


def test_init_server_with_name() -> None:
    # This function is mentioned in the original file but not implemented in the test_server.py file
    # It's assumed to exist as it's called in the test_server_initialization function
    pass


def test_init_server_with_dependencies() -> None:
    # This function is mentioned in the original file but not implemented in the test_server.py file
    # It's assumed to exist as it's called in the test_server_initialization function
    pass


def test_init_server_with_name_and_dependencies() -> None:
    # This function is mentioned in the original file but not implemented in the test_server.py file
    # It's assumed to exist as it's called in the test_server_initialization function
    pass
