"""
Token API implementation for Ankr Advanced API
"""

from typing import Any, Dict, Optional

from ankr import AnkrWeb3
from pydantic import BaseModel

from ..constants import (
    TOKEN_GET_ACCOUNT_BALANCE,
    TOKEN_GET_CURRENCIES,
    TOKEN_GET_TOKEN_HOLDERS,
    TOKEN_GET_TOKEN_HOLDERS_COUNT,
    TOKEN_GET_TOKEN_PRICE,
    TOKEN_GET_TOKEN_TRANSFERS,
)


class AccountBalanceRequest(BaseModel):
    wallet_address: str
    blockchain: Optional[str] = None
    erc20_only: Optional[bool] = None
    native_only: Optional[bool] = None
    tokens_only: Optional[bool] = None


class CurrenciesRequest(BaseModel):
    blockchain: Optional[str] = None
    page_token: Optional[str] = None
    page_size: Optional[int] = 50


class TokenPriceRequest(BaseModel):
    blockchain: str
    contract_address: str


class TokenHoldersRequest(BaseModel):
    blockchain: str
    contract_address: str
    page_token: Optional[str] = None
    page_size: Optional[int] = 50


class TokenHoldersCountRequest(BaseModel):
    blockchain: str
    contract_address: str


class TokenTransfersRequest(BaseModel):
    blockchain: str
    contract_address: Optional[str] = None
    wallet_address: Optional[str] = None
    from_block: Optional[int] = None
    to_block: Optional[int] = None
    page_token: Optional[str] = None
    page_size: Optional[int] = 50


class TokenApi:
    """Wrapper for Ankr Token API methods"""

    def __init__(self, client: AnkrWeb3):
        self.client = client

    async def get_account_balance(self, request: AccountBalanceRequest) -> Dict[str, Any]:
        """Get token balances for a wallet"""
        from ankr.types import GetAccountBalanceRequest
        
        ankr_request = GetAccountBalanceRequest(
            wallet_address=request.wallet_address,
            blockchain=request.blockchain
        )
        
        result = self.client.token.get_account_balance(ankr_request)
        if hasattr(result, "__iter__"):
            assets = list(result) if result else []
            return {"assets": assets}

    async def get_currencies(self, request: CurrenciesRequest) -> Dict[str, Any]:
        """Get available currencies"""
        from ankr.types import GetCurrenciesRequest
        
        ankr_request = GetCurrenciesRequest(
            blockchain=request.blockchain,
            page_token=request.page_token,
            page_size=request.page_size
        )
        
        result = self.client.token.get_currencies(ankr_request)
        if hasattr(result, "__iter__"):
            currencies = list(result) if result else []
            return {"currencies": currencies}

    async def get_token_price(self, request: TokenPriceRequest) -> Dict[str, Any]:
        """Get token price information"""
        from ankr.types import GetTokenPriceRequest
        
        ankr_request = GetTokenPriceRequest(
            blockchain=request.blockchain,
            contract_address=request.contract_address
        )
        
        result = self.client.token.get_token_price(ankr_request)
        if hasattr(result, "__dict__"):
            return result.__dict__
        return {"price_usd": str(result)}

    async def get_token_holders(self, request: TokenHoldersRequest) -> Dict[str, Any]:
        """Get token holders"""
        from ankr.types import GetTokenHoldersRequest
        
        ankr_request = GetTokenHoldersRequest(
            blockchain=request.blockchain,
            contract_address=request.contract_address,
            page_token=request.page_token,
            page_size=request.page_size
        )
        
        result = self.client.token.get_token_holders(ankr_request)
        if hasattr(result, "__dict__"):
            return result.__dict__
        if hasattr(result, "__iter__"):
            holders = list(result) if result else []
            return {"holders": holders}

    async def get_token_holders_count(self, request: TokenHoldersCountRequest) -> Dict[str, Any]:
        """Get token holders count"""
        from ankr.types import GetTokenHoldersCountRequest
        
        ankr_request = GetTokenHoldersCountRequest(
            blockchain=request.blockchain,
            contract_address=request.contract_address
        )
        
        result = self.client.token.get_token_holders_count(ankr_request)
        if hasattr(result, "__dict__"):
            return result.__dict__
        return {"count": int(result) if result else 0}

    async def get_token_transfers(self, request: TokenTransfersRequest) -> Dict[str, Any]:
        """Get token transfer history"""
        from ankr.types import GetTokenTransfersRequest
        
        ankr_request = GetTokenTransfersRequest(
            blockchain=request.blockchain,
            contract_address=request.contract_address,
            wallet_address=request.wallet_address,
            from_block=request.from_block,
            to_block=request.to_block,
            page_token=request.page_token,
            page_size=request.page_size
        )
        
        result = self.client.token.get_token_transfers(ankr_request)
        if hasattr(result, "__dict__"):
            return result.__dict__
        if hasattr(result, "__iter__"):
            transfers = list(result) if result else []
            return {"transfers": transfers}
