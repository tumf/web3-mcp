"""
Tests for FastMCP server
"""

import os
import pytest
from unittest.mock import patch, MagicMock

from web3_mcp.server import FastMCP
from web3_mcp.constants import SUPPORTED_NETWORKS

@pytest.fixture
def mock_ankr_web3():
    """Mock AnkrWeb3 client"""
    with patch("web3_mcp.auth.AnkrWeb3") as mock:
        mock_client = MagicMock()
        mock.return_value = mock_client
        yield mock_client

def test_server_initialization(mock_ankr_web3):
    """Test server initialization"""
    server = FastMCP(
        name="Test Server",
        endpoint="https://test.endpoint",
        private_key="test_key"
    )
    
    assert server.mcp.name == "Test Server"
    
    assert server.nft_api is not None
    assert server.query_api is not None
    assert server.token_api is not None

def test_utility_tools():
    """Test utility tools"""
    with patch("web3_mcp.auth.AnkrWeb3"):
        server = FastMCP(
            name="Test Server",
            endpoint="https://test.endpoint",
            private_key="test_key"
        )
        
        mcp = server()
        
        tools = mcp.list_tools()
        
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
        
        tool_names = [tool.name for tool in tools]
        for expected_tool in expected_tools:
            assert expected_tool in tool_names
        
        resources = mcp.list_resources()
        resource_uris = [resource.uri for resource in resources]
        assert "ankr://info" in resource_uris
