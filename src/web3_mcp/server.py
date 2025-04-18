"""
MCP server implementation for Ankr Advanced API
"""

from typing import Any, Dict, List, Optional

from fastmcp import FastMCP

from .api.nft import (
    NFTApi,
    NFTByOwnerRequest,
    NFTHoldersRequest,
    NFTMetadataRequest,
    NFTTransfersRequest,
)
from .api.query import (
    BlockchainStatsRequest,
    BlocksRequest,
    InteractionsRequest,
    LogsRequest,
    QueryApi,
    TransactionsByAddressRequest,
    TransactionsByHashRequest,
)
from .api.token import (
    AccountBalanceRequest,
    CurrenciesRequest,
    CurrenciesResponse,
    TokenApi,
    TokenHoldersCountRequest,
    TokenHoldersCountResponse,
    TokenHoldersRequest,
    TokenHoldersResponse,
    TokenPriceRequest,
    TokenTransfersRequest,
    TokenTransfersResponse,
)
from .auth import AnkrAuth
from .constants import SUPPORTED_NETWORKS

# Initialize authentication
_auth = None


def init_server(
    name: str = "Ankr MCP", endpoint: Optional[str] = None, private_key: Optional[str] = None
) -> FastMCP:
    """
    Initialize the MCP server

    Args:
        name: Server name
        endpoint: Ankr RPC endpoint (defaults to ANKR_ENDPOINT env var)
        private_key: Private key for authentication (defaults to ANKR_PRIVATE_KEY env var)

    Returns:
        Initialized FastMCP server instance
    """
    global _auth

    # Initialize authentication
    _auth = AnkrAuth(endpoint, private_key)

    # Create MCP server
    mcp: FastMCP = FastMCP(name, dependencies=["ankr-sdk>=1.0.2"])

    # Initialize API clients
    nft_api = NFTApi(_auth.client)
    query_api = QueryApi(_auth.client)
    token_api = TokenApi(_auth.client)

    @mcp.tool()
    async def get_nfts_by_owner(request: NFTByOwnerRequest) -> Dict[str, Any]:
        """
        Get NFTs owned by a wallet address

        Args:
            request: NFT by owner request parameters

        Returns:
            List of NFTs owned by the specified wallet
        """
        return await nft_api.get_nfts_by_owner(request)

    @mcp.tool()
    async def get_nft_metadata(request: NFTMetadataRequest) -> Dict[str, Any]:
        """
        Get metadata for a specific NFT

        Args:
            request: NFT metadata request parameters

        Returns:
            NFT metadata information
        """
        return await nft_api.get_nft_metadata(request)

    @mcp.tool()
    async def get_nft_holders(request: NFTHoldersRequest) -> Dict[str, Any]:
        """
        Get holders of a specific NFT collection

        Args:
            request: NFT holders request parameters

        Returns:
            List of NFT holders for the collection
        """
        return await nft_api.get_nft_holders(request)

    # NFT Transfers endpoint is not supported in the current API
    # @mcp.tool()
    async def get_nft_transfers(request: NFTTransfersRequest) -> Dict[str, Any]:
        """
        Get transfer history for NFTs

        Args:
            request: NFT transfers request parameters

        Returns:
            List of NFT transfers matching the criteria
        """
        return await nft_api.get_nft_transfers(request)

    @mcp.tool()
    async def get_blockchain_stats(request: BlockchainStatsRequest) -> Dict[str, Any]:
        """
        Get blockchain statistics

        Args:
            request: Blockchain stats request parameters

        Returns:
            Statistics for the specified blockchain
        """
        return await query_api.get_blockchain_stats(request)

    @mcp.tool()
    async def get_blocks(request: BlocksRequest) -> Dict[str, Any]:
        """
        Get blocks information

        Args:
            request: Blocks request parameters

        Returns:
            List of blocks matching the criteria
        """
        return await query_api.get_blocks(request)

    @mcp.tool()
    async def get_logs(request: LogsRequest) -> Dict[str, Any]:
        """
        Get blockchain logs

        Args:
            request: Logs request parameters

        Returns:
            List of logs matching the criteria
        """
        return await query_api.get_logs(request)

    # Transactions by hash endpoint is not supported in the current API
    # @mcp.tool()
    async def get_transactions_by_hash(request: TransactionsByHashRequest) -> Dict[str, Any]:
        """
        Get transactions by hash

        Args:
            request: Transactions by hash request parameters

        Returns:
            Transaction details for the specified hash
        """
        return await query_api.get_transactions_by_hash(request)

    # Transactions by address endpoint is not supported in the current API
    # @mcp.tool()
    async def get_transactions_by_address(request: TransactionsByAddressRequest) -> Dict[str, Any]:
        """
        Get transactions by address

        Args:
            request: Transactions by address request parameters

        Returns:
            List of transactions for the specified address
        """
        return await query_api.get_transactions_by_address(request)

    # Interactions endpoint is not supported in the current API
    # @mcp.tool()
    async def get_interactions(request: InteractionsRequest) -> Dict[str, Any]:
        """
        Get wallet interactions with contracts

        Args:
            request: Interactions request parameters

        Returns:
            List of interactions matching the criteria
        """
        return await query_api.get_interactions(request)

    @mcp.tool()
    async def get_account_balance(request: AccountBalanceRequest) -> Dict[str, Any]:
        """
        Get token balances for a wallet address

        Args:
            request: Account balance request parameters

        Returns:
            Token balances for the specified wallet
        """
        return await token_api.get_account_balance(request)

    # Currencies endpoint is not supported in the current API
    # @mcp.tool()
    async def get_currencies(request: CurrenciesRequest) -> CurrenciesResponse:
        """
        Get available currencies

        Args:
            request: Currencies request parameters

        Returns:
            List of available currencies
        """
        return await token_api.get_currencies(request)

    @mcp.tool()
    async def get_token_price(request: TokenPriceRequest) -> Dict[str, Any]:
        """
        Get token price information

        Args:
            request: Token price request parameters

        Returns:
            Price information for the specified token
        """
        return await token_api.get_token_price(request)

    # Token Holders endpoint is not provided as a tool
    # @mcp.tool()
    async def get_token_holders(request: TokenHoldersRequest) -> TokenHoldersResponse:
        """
        Get token holders

        Args:
            request: Token holders request parameters

        Returns:
            List of holders for the specified token
        """
        return await token_api.get_token_holders(request)

    # Token Holders Count endpoint is not supported in the current API
    # @mcp.tool()
    async def get_token_holders_count(
        request: TokenHoldersCountRequest,
    ) -> TokenHoldersCountResponse:
        """
        Get token holders count

        Args:
            request: Token holders count request parameters

        Returns:
            Holder count for the specified token
        """
        return await token_api.get_token_holders_count(request)

    # Token Transfers endpoint is not supported in the current API
    # @mcp.tool()
    async def get_token_transfers(request: TokenTransfersRequest) -> TokenTransfersResponse:
        """
        Get token transfer history

        Args:
            request: Token transfers request parameters

        Returns:
            List of token transfers matching the criteria
        """
        return await token_api.get_token_transfers(request)

    @mcp.tool()
    def get_supported_networks() -> List[str]:
        """
        Get a list of supported blockchain networks

        Returns:
            List of supported blockchain network identifiers
        """
        return SUPPORTED_NETWORKS

    @mcp.resource("ankr://info")
    def get_ankr_info() -> Dict[str, Any]:
        """
        Get information about Ankr Advanced API

        Returns:
            Information about the Ankr Advanced API
        """
        return {
            "name": "Ankr Advanced API",
            "description": "Multi-chain Web3 data API providing access to NFT, Token and Query data",
            "documentation": "https://www.ankr.com/docs/advanced-api/overview/",
            "supported_networks": SUPPORTED_NETWORKS,
            "api_categories": ["NFT API", "Query API", "Token API"],
        }

    return mcp
