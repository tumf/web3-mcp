"""
FastMCP server implementation for Ankr Advanced API
"""

import os
from typing import Any, Dict, List, Optional, cast

from fastmcp import FastMCP, Context
from pydantic import BaseModel

from .auth import AnkrAuth
from .api.nft import (
    NFTApi,
    NFTByOwnerRequest,
    NFTMetadataRequest,
    NFTHoldersRequest,
    NFTTransfersRequest,
)
from .api.query import (
    QueryApi,
    BlockchainStatsRequest,
    BlocksRequest,
    LogsRequest,
    TransactionsByHashRequest,
    TransactionsByAddressRequest,
    InteractionsRequest,
)
from .api.token import (
    TokenApi,
    AccountBalanceRequest,
    CurrenciesRequest,
    TokenPriceRequest,
    TokenHoldersRequest,
    TokenHoldersCountRequest,
    TokenTransfersRequest,
)
from .constants import SUPPORTED_NETWORKS

class FastMCP:
    """FastMCP server implementation wrapping Ankr Advanced API"""
    
    def __init__(
        self,
        name: str = "FastMCP",
        endpoint: Optional[str] = None,
        private_key: Optional[str] = None,
    ):
        """
        Initialize FastMCP server
        
        Args:
            name: Server name
            endpoint: Ankr RPC endpoint (defaults to ANKR_ENDPOINT env var)
            private_key: Private key for authentication (defaults to ANKR_PRIVATE_KEY env var)
        """
        self.auth = AnkrAuth(endpoint, private_key)
        self.mcp = FastMCP(name, dependencies=["ankr-sdk>=1.0.2"])
        
        self.nft_api = NFTApi(self.auth.client)
        self.query_api = QueryApi(self.auth.client)
        self.token_api = TokenApi(self.auth.client)
        
        self._register_nft_tools()
        self._register_query_tools()
        self._register_token_tools()
        self._register_utility_tools()
    
    def _register_nft_tools(self) -> None:
        """Register NFT API tools"""
        
        @self.mcp.tool()
        async def get_nfts_by_owner(request: NFTByOwnerRequest) -> Dict[str, Any]:
            """
            Get NFTs owned by a wallet address
            
            Args:
                request: NFT by owner request parameters
            
            Returns:
                List of NFTs owned by the specified wallet
            """
            return await self.nft_api.get_nfts_by_owner(request)
        
        @self.mcp.tool()
        async def get_nft_metadata(request: NFTMetadataRequest) -> Dict[str, Any]:
            """
            Get metadata for a specific NFT
            
            Args:
                request: NFT metadata request parameters
            
            Returns:
                NFT metadata information
            """
            return await self.nft_api.get_nft_metadata(request)
        
        @self.mcp.tool()
        async def get_nft_holders(request: NFTHoldersRequest) -> Dict[str, Any]:
            """
            Get holders of a specific NFT collection
            
            Args:
                request: NFT holders request parameters
            
            Returns:
                List of NFT holders for the collection
            """
            return await self.nft_api.get_nft_holders(request)
        
        @self.mcp.tool()
        async def get_nft_transfers(request: NFTTransfersRequest) -> Dict[str, Any]:
            """
            Get transfer history for NFTs
            
            Args:
                request: NFT transfers request parameters
            
            Returns:
                List of NFT transfers matching the criteria
            """
            return await self.nft_api.get_nft_transfers(request)
    
    def _register_query_tools(self) -> None:
        """Register Query API tools"""
        
        @self.mcp.tool()
        async def get_blockchain_stats(request: BlockchainStatsRequest) -> Dict[str, Any]:
            """
            Get blockchain statistics
            
            Args:
                request: Blockchain stats request parameters
            
            Returns:
                Statistics for the specified blockchain
            """
            return await self.query_api.get_blockchain_stats(request)
        
        @self.mcp.tool()
        async def get_blocks(request: BlocksRequest) -> Dict[str, Any]:
            """
            Get blocks information
            
            Args:
                request: Blocks request parameters
            
            Returns:
                List of blocks matching the criteria
            """
            return await self.query_api.get_blocks(request)
        
        @self.mcp.tool()
        async def get_logs(request: LogsRequest) -> Dict[str, Any]:
            """
            Get blockchain logs
            
            Args:
                request: Logs request parameters
            
            Returns:
                List of logs matching the criteria
            """
            return await self.query_api.get_logs(request)
        
        @self.mcp.tool()
        async def get_transactions_by_hash(request: TransactionsByHashRequest) -> Dict[str, Any]:
            """
            Get transactions by hash
            
            Args:
                request: Transactions by hash request parameters
            
            Returns:
                Transaction details for the specified hash
            """
            return await self.query_api.get_transactions_by_hash(request)
        
        @self.mcp.tool()
        async def get_transactions_by_address(request: TransactionsByAddressRequest) -> Dict[str, Any]:
            """
            Get transactions by address
            
            Args:
                request: Transactions by address request parameters
            
            Returns:
                List of transactions for the specified address
            """
            return await self.query_api.get_transactions_by_address(request)
        
        @self.mcp.tool()
        async def get_interactions(request: InteractionsRequest) -> Dict[str, Any]:
            """
            Get wallet interactions with contracts
            
            Args:
                request: Interactions request parameters
            
            Returns:
                List of interactions matching the criteria
            """
            return await self.query_api.get_interactions(request)
    
    def _register_token_tools(self) -> None:
        """Register Token API tools"""
        
        @self.mcp.tool()
        async def get_account_balance(request: AccountBalanceRequest) -> Dict[str, Any]:
            """
            Get token balances for a wallet
            
            Args:
                request: Account balance request parameters
            
            Returns:
                Token balances for the specified wallet
            """
            return await self.token_api.get_account_balance(request)
        
        @self.mcp.tool()
        async def get_currencies(request: CurrenciesRequest) -> Dict[str, Any]:
            """
            Get available currencies
            
            Args:
                request: Currencies request parameters
            
            Returns:
                List of available currencies
            """
            return await self.token_api.get_currencies(request)
        
        @self.mcp.tool()
        async def get_token_price(request: TokenPriceRequest) -> Dict[str, Any]:
            """
            Get token price information
            
            Args:
                request: Token price request parameters
            
            Returns:
                Price information for the specified token
            """
            return await self.token_api.get_token_price(request)
        
        @self.mcp.tool()
        async def get_token_holders(request: TokenHoldersRequest) -> Dict[str, Any]:
            """
            Get token holders
            
            Args:
                request: Token holders request parameters
            
            Returns:
                List of holders for the specified token
            """
            return await self.token_api.get_token_holders(request)
        
        @self.mcp.tool()
        async def get_token_holders_count(request: TokenHoldersCountRequest) -> Dict[str, Any]:
            """
            Get token holders count
            
            Args:
                request: Token holders count request parameters
            
            Returns:
                Holder count for the specified token
            """
            return await self.token_api.get_token_holders_count(request)
        
        @self.mcp.tool()
        async def get_token_transfers(request: TokenTransfersRequest) -> Dict[str, Any]:
            """
            Get token transfer history
            
            Args:
                request: Token transfers request parameters
            
            Returns:
                List of token transfers matching the criteria
            """
            return await self.token_api.get_token_transfers(request)
    
    def _register_utility_tools(self) -> None:
        """Register utility tools"""
        
        @self.mcp.tool()
        def get_supported_networks() -> List[str]:
            """
            Get a list of supported blockchain networks
            
            Returns:
                List of supported blockchain network identifiers
            """
            return SUPPORTED_NETWORKS
        
        @self.mcp.resource("ankr://info")
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
                "api_categories": [
                    "NFT API", 
                    "Query API", 
                    "Token API"
                ]
            }
    
    def run(self, **kwargs: Any) -> None:
        """Run the FastMCP server"""
        self.mcp.run(**kwargs)
    
    def __call__(self) -> FastMCP:
        """Return the FastMCP server instance"""
        return self.mcp
