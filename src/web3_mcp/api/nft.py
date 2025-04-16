"""
NFT API implementation for Ankr Advanced API
"""

from typing import Any, Dict, List, Optional

from ankr import AnkrWeb3
from pydantic import BaseModel, Field

from ..constants import (
    NFT_GET_BY_OWNER,
    NFT_GET_METADATA,
    NFT_GET_HOLDERS,
    NFT_GET_TRANSFERS,
)

class NFTCollection(BaseModel):
    blockchain: str
    name: str = Field(default="")
    collection_id: str = Field(default="")
    contract_address: str

class NFTMetadata(BaseModel):
    blockchain: str
    contract_address: str
    token_id: str
    token_url: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    attributes: Optional[List[Dict[str, Any]]] = None

class NFTByOwnerRequest(BaseModel):
    wallet_address: str
    blockchain: Optional[str] = None
    page_token: Optional[str] = None
    page_size: Optional[int] = 50

class NFTMetadataRequest(BaseModel):
    blockchain: str
    contract_address: str
    token_id: str

class NFTHoldersRequest(BaseModel):
    blockchain: str
    contract_address: str
    page_token: Optional[str] = None
    page_size: Optional[int] = 50

class NFTTransfersRequest(BaseModel):
    blockchain: str
    contract_address: Optional[str] = None
    token_id: Optional[str] = None
    wallet_address: Optional[str] = None
    from_block: Optional[int] = None
    to_block: Optional[int] = None
    page_token: Optional[str] = None
    page_size: Optional[int] = 50

class NFTApi:
    """Wrapper for Ankr NFT API methods"""
    
    def __init__(self, client: AnkrWeb3):
        self.client = client
    
    async def get_nfts_by_owner(self, request: NFTByOwnerRequest) -> Dict[str, Any]:
        """Get NFTs owned by a wallet address"""
        params = request.model_dump(exclude_none=True)
        return await self.client.full_request(NFT_GET_BY_OWNER, params)
    
    async def get_nft_metadata(self, request: NFTMetadataRequest) -> Dict[str, Any]:
        """Get metadata for a specific NFT"""
        params = request.model_dump(exclude_none=True)
        return await self.client.full_request(NFT_GET_METADATA, params)
    
    async def get_nft_holders(self, request: NFTHoldersRequest) -> Dict[str, Any]:
        """Get holders of a specific NFT collection"""
        params = request.model_dump(exclude_none=True)
        return await self.client.full_request(NFT_GET_HOLDERS, params)
    
    async def get_nft_transfers(self, request: NFTTransfersRequest) -> Dict[str, Any]:
        """Get transfer history for NFTs"""
        params = request.model_dump(exclude_none=True)
        return await self.client.full_request(NFT_GET_TRANSFERS, params)
