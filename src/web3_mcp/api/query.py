"""
Query API implementation for Ankr Advanced API
"""

from typing import Any, Dict, List, Optional, Union

from ankr import AnkrWeb3
from pydantic import BaseModel, Field

from ..constants import (
    QUERY_GET_BLOCKCHAIN_STATS,
    QUERY_GET_BLOCKS,
    QUERY_GET_LOGS,
    QUERY_GET_TRANSACTIONS_BY_HASH,
    QUERY_GET_TRANSACTIONS_BY_ADDRESS,
    QUERY_GET_INTERACTIONS,
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
        params = request.model_dump(exclude_none=True)
        return await self.client.full_request(QUERY_GET_BLOCKCHAIN_STATS, params)
    
    async def get_blocks(self, request: BlocksRequest) -> Dict[str, Any]:
        """Get blocks information"""
        params = request.model_dump(exclude_none=True)
        return await self.client.full_request(QUERY_GET_BLOCKS, params)
    
    async def get_logs(self, request: LogsRequest) -> Dict[str, Any]:
        """Get blockchain logs"""
        params = request.model_dump(exclude_none=True)
        return await self.client.full_request(QUERY_GET_LOGS, params)
    
    async def get_transactions_by_hash(self, request: TransactionsByHashRequest) -> Dict[str, Any]:
        """Get transactions by hash"""
        params = request.model_dump(exclude_none=True)
        return await self.client.full_request(QUERY_GET_TRANSACTIONS_BY_HASH, params)
    
    async def get_transactions_by_address(self, request: TransactionsByAddressRequest) -> Dict[str, Any]:
        """Get transactions by address"""
        params = request.model_dump(exclude_none=True)
        return await self.client.full_request(QUERY_GET_TRANSACTIONS_BY_ADDRESS, params)
    
    async def get_interactions(self, request: InteractionsRequest) -> Dict[str, Any]:
        """Get wallet interactions with contracts"""
        params = request.model_dump(exclude_none=True)
        return await self.client.full_request(QUERY_GET_INTERACTIONS, params)
