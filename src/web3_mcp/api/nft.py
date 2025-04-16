"""
NFT API implementation for Ankr Advanced API
"""

from typing import Any, Dict, List, Optional

from ankr import AnkrWeb3
from pydantic import BaseModel, Field

from ..constants import (
    NFT_GET_BY_OWNER,
    NFT_GET_HOLDERS,
    NFT_GET_METADATA,
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
        from ankr.types import GetNFTsByOwnerRequest
        
        wallet_address = request.wallet_address
        blockchain = request.blockchain if request.blockchain else None
        page_token = request.page_token if request.page_token else None
        
        ankr_request = GetNFTsByOwnerRequest(
            walletAddress=wallet_address,
            blockchain=blockchain
        )
        
        if request.page_size is not None:
            ankr_request.pageSize = request.page_size
            
        if page_token:
            ankr_request.pageToken = page_token
        
        result = self.client.nft.get_nfts(ankr_request)
        assets = list(result) if result else []
        return {"assets": assets, "next_page_token": ""}

    async def get_nft_metadata(self, request: NFTMetadataRequest) -> Dict[str, Any]:
        """Get metadata for a specific NFT"""
        from ankr.types import GetNFTMetadataRequest
        
        ankr_request = GetNFTMetadataRequest(
            blockchain=request.blockchain,
            contractAddress=request.contract_address,
            tokenId=request.token_id,
            forceFetch=True
        )
        
        result = self.client.nft.get_nft_metadata(ankr_request)
        if hasattr(result, "__dict__"):
            return result.__dict__
        return {
            "name": getattr(result, "name", ""),
            "description": getattr(result, "description", ""),
            "image": getattr(result, "image", ""),
            "attributes": getattr(result, "attributes", [])
        }

    async def get_nft_holders(self, request: NFTHoldersRequest) -> Dict[str, Any]:
        """Get holders of a specific NFT collection"""
        from ankr.types import GetNFTHoldersRequest
        
        ankr_request = GetNFTHoldersRequest(
            blockchain=request.blockchain,
            contractAddress=request.contract_address,
            pageToken=request.page_token,
            pageSize=request.page_size
        )
        
        result = self.client.nft.get_nft_holders(ankr_request)
        if hasattr(result, "__dict__"):
            return result.__dict__
        
        if hasattr(result, "__iter__"):
            holders = list(result) if result else []
            return {"holders": holders}

    async def get_nft_transfers(self, request: NFTTransfersRequest) -> Dict[str, Any]:
        """Get transfer history for NFTs"""
        from ankr.types import GetNFTTransfersRequest
        
        ankr_request = GetNFTTransfersRequest(
            blockchain=request.blockchain,
            contractAddress=request.contract_address,
            tokenId=request.token_id,
            walletAddress=request.wallet_address,
            fromBlock=request.from_block,
            toBlock=request.to_block,
            pageToken=request.page_token,
            pageSize=request.page_size
        )
        
        result = self.client.nft.get_nft_transfers(ankr_request)
        if hasattr(result, "__dict__"):
            return result.__dict__
        
        if hasattr(result, "__iter__"):
            transfers = list(result) if result else []
            return {"transfers": transfers}
