"""
Query API implementation for Ankr Advanced API
"""

from typing import Any, Dict, List, Optional

from ankr import AnkrWeb3
from pydantic import BaseModel

from ..constants import (
    QUERY_GET_BLOCKCHAIN_STATS,
    QUERY_GET_BLOCKS,
    QUERY_GET_INTERACTIONS,
    QUERY_GET_LOGS,
    QUERY_GET_TRANSACTIONS_BY_ADDRESS,
    QUERY_GET_TRANSACTIONS_BY_HASH,
)


class BlockchainStatsRequest(BaseModel):
    blockchain: str


class BlocksRequest(BaseModel):
    blockchain: str
    from_block: Optional[int] = None
    to_block: Optional[int] = None
    descending_order: Optional[bool] = None
    page_token: Optional[str] = None
    page_size: Optional[int] = 50


class LogsRequest(BaseModel):
    blockchain: str
    from_block: Optional[int] = None
    to_block: Optional[int] = None
    address: Optional[str] = None
    topics: Optional[List[str]] = None
    descending_order: Optional[bool] = None
    page_token: Optional[str] = None
    page_size: Optional[int] = 50


class TransactionsByHashRequest(BaseModel):
    blockchain: str
    transaction_hash: str


class TransactionsByAddressRequest(BaseModel):
    blockchain: str
    wallet_address: str
    from_block: Optional[int] = None
    to_block: Optional[int] = None
    descending_order: Optional[bool] = None
    page_token: Optional[str] = None
    page_size: Optional[int] = 50


class InteractionsRequest(BaseModel):
    blockchain: str
    wallet_address: str
    from_block: Optional[int] = None
    to_block: Optional[int] = None
    contract_address: Optional[str] = None
    descending_order: Optional[bool] = None
    page_token: Optional[str] = None
    page_size: Optional[int] = 50


class QueryApi:
    """Wrapper for Ankr Query API methods"""

    def __init__(self, client: AnkrWeb3):
        self.client = client

    async def get_blockchain_stats(self, request: BlockchainStatsRequest) -> Dict[str, Any]:
        """Get blockchain statistics"""
        from ankr.types import GetBlockchainStatsRequest
        
        ankr_request = GetBlockchainStatsRequest(
            blockchain=request.blockchain
        )
        
        result = await self.client.query.get_blockchain_stats(ankr_request)
        return result

    async def get_blocks(self, request: BlocksRequest) -> Dict[str, Any]:
        """Get blocks information"""
        from ankr.types import GetBlocksRequest
        
        ankr_request = GetBlocksRequest(
            blockchain=request.blockchain,
            fromBlock=request.from_block,
            toBlock=request.to_block,
            descendingOrder=request.descending_order,
            pageToken=request.page_token,
            pageSize=request.page_size
        )
        
        return await self.client.query.get_blocks(ankr_request)

    async def get_logs(self, request: LogsRequest) -> Dict[str, Any]:
        """Get blockchain logs"""
        from ankr.types import GetLogsRequest
        
        ankr_request = GetLogsRequest(
            blockchain=request.blockchain,
            fromBlock=request.from_block,
            toBlock=request.to_block,
            address=request.address,
            topics=request.topics,
            descendingOrder=request.descending_order,
            pageToken=request.page_token,
            pageSize=request.page_size
        )
        
        return await self.client.query.get_logs(ankr_request)

    async def get_transactions_by_hash(self, request: TransactionsByHashRequest) -> Dict[str, Any]:
        """Get transactions by hash"""
        from ankr.types import GetTransactionByHashRequest
        
        ankr_request = GetTransactionByHashRequest(
            blockchain=request.blockchain,
            transactionHash=request.transaction_hash
        )
        
        return await self.client.query.get_transaction_by_hash(ankr_request)

    async def get_transactions_by_address(
        self, request: TransactionsByAddressRequest
    ) -> Dict[str, Any]:
        """Get transactions by address"""
        from ankr.types import GetTransactionsByAddressRequest
        
        ankr_request = GetTransactionsByAddressRequest(
            blockchain=request.blockchain,
            walletAddress=request.wallet_address,
            fromBlock=request.from_block,
            toBlock=request.to_block,
            descendingOrder=request.descending_order,
            pageToken=request.page_token,
            pageSize=request.page_size
        )
        
        return await self.client.query.get_transactions_by_address(ankr_request)

    async def get_interactions(self, request: InteractionsRequest) -> Dict[str, Any]:
        """Get wallet interactions with contracts"""
        from ankr.types import GetInteractionsRequest
        
        ankr_request = GetInteractionsRequest(
            blockchain=request.blockchain,
            walletAddress=request.wallet_address,
            fromBlock=request.from_block,
            toBlock=request.to_block,
            contractAddress=request.contract_address,
            descendingOrder=request.descending_order,
            pageToken=request.page_token,
            pageSize=request.page_size
        )
        
        return await self.client.query.get_interactions(ankr_request)
