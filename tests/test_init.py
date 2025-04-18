"""
Test server initialization
"""

import os
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest

from web3_mcp.server import init_server


@pytest.fixture(autouse=True)
def mock_env() -> Generator[None, None, None]:
    """Set up environment variables for tests"""
    with patch.dict(
        os.environ, {"ANKR_ENDPOINT": "https://test.endpoint", "ANKR_PRIVATE_KEY": "test_key"}
    ):
        yield


@pytest.mark.asyncio
@patch("web3_mcp.auth.AnkrWeb3")
async def test_server_init(mock_ankr_web3: MagicMock) -> None:
    """Test server initialization with mock endpoint"""
    mcp = init_server(name="Test Server")

    assert mcp.name == "Test Server"

    tools = await mcp.get_tools()
    tool_names = list(tools.keys())

    assert "get_nfts_by_owner" in tool_names
    assert "get_blockchain_stats" in tool_names
    assert "get_account_balance" in tool_names
