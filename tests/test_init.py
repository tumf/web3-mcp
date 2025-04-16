"""
Test server initialization
"""

import unittest
from unittest.mock import patch

from web3_mcp.server import FastMCP

class TestServerInit(unittest.TestCase):
    """Test server initialization"""
    
    @patch("web3_mcp.auth.AnkrWeb3")
    def test_server_init(self, mock_ankr_web3):
        """Test server initialization with mock endpoint"""
        server = FastMCP(
            name="Test Server",
            endpoint="https://test.endpoint",
            private_key="test_key"
        )
        
        self.assertEqual(server.mcp.name, "Test Server")
        
        self.assertIsNotNone(server.nft_api)
        self.assertIsNotNone(server.query_api)
        self.assertIsNotNone(server.token_api)

if __name__ == "__main__":
    unittest.main()
