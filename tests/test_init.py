"""
Test server initialization
"""

import os
import unittest
from unittest.mock import MagicMock, patch

from web3_mcp.server import init_server


class TestServerInit(unittest.TestCase):
    """Test server initialization"""

    def setUp(self) -> None:
        """Set up test environment"""
        self.env_patcher = patch.dict(
            os.environ, {"ANKR_ENDPOINT": "https://test.endpoint", "ANKR_PRIVATE_KEY": "test_key"}
        )
        self.env_patcher.start()
        self.addCleanup(self.env_patcher.stop)

    @patch("web3_mcp.auth.AnkrWeb3")
    def test_server_init(self, mock_ankr_web3: MagicMock) -> None:
        """Test server initialization with mock endpoint"""
        mcp = init_server(name="Test Server")

        self.assertEqual(mcp.name, "Test Server")

        tools = mcp.list_tools()
        tool_names = [tool.name for tool in tools]

        self.assertIn("get_nfts_by_owner", tool_names)
        self.assertIn("get_blockchain_stats", tool_names)
        self.assertIn("get_account_balance", tool_names)


if __name__ == "__main__":
    unittest.main()
    unittest.main()
