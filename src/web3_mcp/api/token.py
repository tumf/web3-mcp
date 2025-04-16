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
        params = request.model_dump(exclude_none=True)
        return await self.client.full_request(TOKEN_GET_ACCOUNT_BALANCE, params)

    async def get_currencies(self, request: CurrenciesRequest) -> Dict[str, Any]:
        """Get available currencies"""
        params = request.model_dump(exclude_none=True)
        return await self.client.full_request(TOKEN_GET_CURRENCIES, params)

    async def get_token_price(self, request: TokenPriceRequest) -> Dict[str, Any]:
        """Get token price information"""
        params = request.model_dump(exclude_none=True)
        return await self.client.full_request(TOKEN_GET_TOKEN_PRICE, params)

    async def get_token_holders(self, request: TokenHoldersRequest) -> Dict[str, Any]:
        """Get token holders"""
        params = request.model_dump(exclude_none=True)
        return await self.client.full_request(TOKEN_GET_TOKEN_HOLDERS, params)

    async def get_token_holders_count(self, request: TokenHoldersCountRequest) -> Dict[str, Any]:
        """Get token holders count"""
        params = request.model_dump(exclude_none=True)
        return await self.client.full_request(TOKEN_GET_TOKEN_HOLDERS_COUNT, params)

    async def get_token_transfers(self, request: TokenTransfersRequest) -> Dict[str, Any]:
        """Get token transfer history"""
        params = request.model_dump(exclude_none=True)
        return await self.client.full_request(TOKEN_GET_TOKEN_TRANSFERS, params)
