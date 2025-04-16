"""
Test server initialization
"""

import unittest
from unittest.mock import patch

from web3_mcp.server import init_server

class TestServerInit(unittest.TestCase):
    """Test server initialization"""
    
    @patch("web3_mcp.auth.AnkrWeb3")
    def test_server_init(self, mock_ankr_web3):
        """Test server initialization with mock endpoint"""
        mcp = init_server(
            name="Test Server",
            endpoint="https://test.endpoint",
            private_key="test_key"
        )
        
        self.assertEqual(mcp.name, "Test Server")
        
        tools = mcp.list_tools()
        tool_names = [tool.name for tool in tools]
        
        self.assertIn("get_nfts_by_owner", tool_names)
        self.assertIn("get_blockchain_stats", tool_names)
        self.assertIn("get_account_balance", tool_names)

if __name__ == "__main__":
    unittest.main()
