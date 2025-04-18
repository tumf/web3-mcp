"""
Test fixtures for e2e tests
"""

import os
from typing import Any, AsyncGenerator, Dict, Tuple

import pytest
import pytest_asyncio

from web3_mcp.auth import AnkrAuth


class DirectClient:
    """Client for making requests directly to the Ankr API"""

    def __init__(self, client: Any) -> None:
        self.client = client

    async def call_tool(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """Call a tool method directly on the Ankr API client"""
        request = params or {}

        if tool_name == "get_nfts_by_owner":
            from web3_mcp.api.nft import NFTApi, NFTByOwnerRequest

            return await NFTApi(self.client).get_nfts_by_owner(NFTByOwnerRequest(**request))

        elif tool_name == "get_nft_metadata":
            from web3_mcp.api.nft import NFTApi, NFTMetadataRequest

            return await NFTApi(self.client).get_nft_metadata(NFTMetadataRequest(**request))

        elif tool_name == "get_nft_holders":
            from web3_mcp.api.nft import NFTApi, NFTHoldersRequest

            return await NFTApi(self.client).get_nft_holders(NFTHoldersRequest(**request))

        elif tool_name == "get_nft_transfers":
            from web3_mcp.api.nft import NFTApi, NFTTransfersRequest

            return await NFTApi(self.client).get_nft_transfers(NFTTransfersRequest(**request))

        elif tool_name == "get_blockchain_stats":
            from web3_mcp.api.query import BlockchainStatsRequest, QueryApi

            return await QueryApi(self.client).get_blockchain_stats(
                BlockchainStatsRequest(**request)
            )

        elif tool_name == "get_blocks":
            from web3_mcp.api.query import BlocksRequest, QueryApi

            return await QueryApi(self.client).get_blocks(BlocksRequest(**request))

        elif tool_name == "get_logs":
            from web3_mcp.api.query import LogsRequest, QueryApi

            return await QueryApi(self.client).get_logs(LogsRequest(**request))

        elif tool_name == "get_transactions_by_hash":
            from web3_mcp.api.query import QueryApi, TransactionsByHashRequest

            return await QueryApi(self.client).get_transactions_by_hash(
                TransactionsByHashRequest(**request)
            )

        elif tool_name == "get_transactions_by_address":
            from web3_mcp.api.query import QueryApi, TransactionsByAddressRequest

            return await QueryApi(self.client).get_transactions_by_address(
                TransactionsByAddressRequest(**request)
            )

        elif tool_name == "get_interactions":
            from web3_mcp.api.query import InteractionsRequest, QueryApi

            return await QueryApi(self.client).get_interactions(InteractionsRequest(**request))

        elif tool_name == "get_account_balance":
            from web3_mcp.api.token import AccountBalanceRequest, TokenApi

            return await TokenApi(self.client).get_account_balance(AccountBalanceRequest(**request))

        elif tool_name == "get_token_price":
            from web3_mcp.api.token import TokenApi, TokenPriceRequest

            return await TokenApi(self.client).get_token_price(TokenPriceRequest(**request))

        elif tool_name == "get_currencies":
            from web3_mcp.api.token import CurrenciesRequest, TokenApi

            return await TokenApi(self.client).get_currencies(CurrenciesRequest(**request))

        # Token Holdersエンドポイントはサポートしていないため、コメントアウト
        # elif tool_name == "get_token_holders":
        #     from web3_mcp.api.token import TokenApi, TokenHoldersRequest
        #
        #     return await TokenApi(self.client).get_token_holders(TokenHoldersRequest(**request))

        elif tool_name == "get_token_holders_count":
            from web3_mcp.api.token import TokenApi, TokenHoldersCountRequest

            return await TokenApi(self.client).get_token_holders_count(
                TokenHoldersCountRequest(**request)
            )

        elif tool_name == "get_token_transfers":
            from web3_mcp.api.token import TokenApi, TokenTransfersRequest

            return await TokenApi(self.client).get_token_transfers(TokenTransfersRequest(**request))

        elif tool_name == "get_supported_networks":
            from web3_mcp.constants import SUPPORTED_NETWORKS

            return SUPPORTED_NETWORKS

        else:
            raise ValueError(f"Unknown tool: {tool_name}")


@pytest.fixture(scope="session")
def ankr_credentials() -> Tuple[str, str]:
    """Get Ankr API credentials from environment variables"""
    endpoint = os.environ.get("ANKR_ENDPOINT")
    private_key = os.environ.get("ANKR_PRIVATE_KEY", os.environ.get("DOTENV_PRIVATE_KEY_DEVIN"))

    if not endpoint or not private_key:
        pytest.skip("ANKR_ENDPOINT and ANKR_PRIVATE_KEY environment variables are required")

    return endpoint, private_key


@pytest_asyncio.fixture(scope="session")
async def mcp_client(ankr_credentials: Tuple[str, str]) -> AsyncGenerator[DirectClient, None]:
    """Initialize a client for making requests directly to the Ankr API"""
    endpoint, private_key = ankr_credentials

    # Create auth object with credentials
    auth = AnkrAuth(endpoint=endpoint, private_key=private_key)
    ankr_client = auth.client

    # Create a client that directly uses the API methods
    client = DirectClient(ankr_client)
    yield client
