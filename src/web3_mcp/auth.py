"""
Authentication module for Ankr API
"""

import os
from typing import Optional

from ankr import AnkrWeb3


class AnkrAuth:
    """Authentication handler for Ankr API"""

    def __init__(self, endpoint: Optional[str] = None, private_key: Optional[str] = None):
        """
        Initialize Ankr authentication

        Args:
            endpoint: Ankr RPC endpoint URL (defaults to env var ANKR_ENDPOINT)
            private_key: Private key for authentication (defaults to env var ANKR_PRIVATE_KEY)
        """
        self.endpoint = endpoint or os.environ.get("ANKR_ENDPOINT")
        self.private_key = private_key or os.environ.get(
            "ANKR_PRIVATE_KEY", os.environ.get("DOTENV_PRIVATE_KEY_DEVIN")
        )

        if not self.endpoint:
            raise ValueError("Ankr endpoint not provided. Set ANKR_ENDPOINT environment variable.")

        self._client = None

    @property
    def client(self) -> AnkrWeb3:
        """Return authenticated Ankr client"""
        if not self._client:
            self._client = AnkrWeb3(api_key=self.private_key)
        return self._client
