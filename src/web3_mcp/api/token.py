"""
Token API implementation for Ankr Advanced API
"""

import json
from typing import Any, Dict, List, Optional

from ankr import AnkrWeb3
from pydantic import BaseModel


class AccountBalanceRequest(BaseModel):
    """Request model for getting token balances"""

    wallet_address: str
    blockchain: Optional[str] = None
    page_size: Optional[int] = None
    page_token: Optional[str] = None
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


class AccountBalanceResponse(BaseModel):
    balances: List[Dict[str, Any]]
    next_page_token: str = ""


class CurrenciesResponse(BaseModel):
    currencies: List[Dict[str, Any]]


class TokenPriceResponse(BaseModel):
    prices: List[Dict[str, Any]]


class TokenHoldersResponse(BaseModel):
    holders: List[Dict[str, Any]]
    next_page_token: str = ""


class TokenHoldersCountResponse(BaseModel):
    count: int


class TokenTransfersResponse(BaseModel):
    transfers: List[Dict[str, Any]]
    next_page_token: str = ""


class TokenApi:
    """Wrapper for Ankr Token API methods"""

    def __init__(self, client: AnkrWeb3):
        self.client = client

    async def get_account_balance(self, request: AccountBalanceRequest) -> Dict[str, Any]:
        """Get token balances for a wallet address"""
        from ankr.types import GetAccountBalanceRequest

        ankr_request = GetAccountBalanceRequest(
            walletAddress=request.wallet_address,
            blockchain=request.blockchain,
            pageToken=request.page_token,
            pageSize=request.page_size,
        )

        result = self.client.token.get_account_balance(ankr_request)
        balances = [balance.__dict__ for balance in result] if result else []
        return {"assets": balances}

    async def get_currencies(self, request: CurrenciesRequest) -> CurrenciesResponse:
        """Get available currencies"""
        from ankr.types import GetCurrenciesRequest

        ankr_request = GetCurrenciesRequest(
            blockchain=request.blockchain if request.blockchain else None,
        )

        result = self.client.token.get_currencies(ankr_request)
        currencies = list(result) if result else []
        return CurrenciesResponse(currencies=currencies)

    async def get_token_price(self, request: TokenPriceRequest) -> Dict[str, Any]:
        """Get token price information"""
        from ankr.types import GetTokenPriceRequest

        ankr_request = GetTokenPriceRequest(
            blockchain=request.blockchain,
            contractAddress=request.contract_address,
        )

        result = self.client.token.get_token_price(ankr_request)
        if not result:
            raise ValueError("Failed to get token price: result is None")

        # If result is a string, it's the direct price value
        if isinstance(result, str):
            try:
                price = float(result)
                if price > 0:
                    return {"price_usd": result}
            except ValueError:
                pass

        # Try to parse result as JSON
        try:
            if isinstance(result, str):
                data = json.loads(result)
                if isinstance(data, dict) and "usdPrice" in data:
                    return {"price_usd": str(data["usdPrice"])}
                elif isinstance(data, dict) and "price" in data:
                    return {"price_usd": str(data["price"])}
                elif isinstance(data, dict) and "price_usd" in data:
                    return {"price_usd": str(data["price_usd"])}
        except json.JSONDecodeError:
            pass

        # Try to get price from object attributes
        price_value: Optional[float] = None
        if hasattr(result, "usdPrice"):
            price_value = float(result.usdPrice)
        elif hasattr(result, "price"):
            price_value = float(result.price)
        elif hasattr(result, "price_usd"):
            price_value = float(result.price_usd)

        if price_value is None:
            raise ValueError("Failed to get token price: price not found in response")

        return {"price_usd": str(price_value)}

    async def get_token_holders(self, request: TokenHoldersRequest) -> TokenHoldersResponse:
        """Get token holders"""
        from ankr.types import GetTokenHoldersRequest

        ankr_request = GetTokenHoldersRequest(
            blockchain=request.blockchain,
            contractAddress=request.contract_address,
            pageToken=request.page_token,
            pageSize=request.page_size,
        )

        result = self.client.token.get_token_holders(ankr_request)
        holders = list(result) if result else []
        return TokenHoldersResponse(holders=holders, next_page_token="")

    async def get_token_holders_count(
        self, request: TokenHoldersCountRequest
    ) -> TokenHoldersCountResponse:
        """Get token holders count"""
        from ankr.types import GetTokenHoldersCountRequest

        ankr_request = GetTokenHoldersCountRequest(
            blockchain=request.blockchain,
            contractAddress=request.contract_address,
        )

        result = self.client.token.get_token_holders_count(ankr_request)
        count = result.count if hasattr(result, "count") else 0
        return TokenHoldersCountResponse(count=count)

    async def get_token_transfers(self, request: TokenTransfersRequest) -> TokenTransfersResponse:
        """Get token transfers"""
        from ankr.types import GetTokenTransfersRequest

        ankr_request = GetTokenTransfersRequest(
            blockchain=request.blockchain,
            contractAddress=request.contract_address,
            fromBlock=request.from_block,
            toBlock=request.to_block,
            pageToken=request.page_token,
            pageSize=request.page_size,
        )

        result = self.client.token.get_token_transfers(ankr_request)
        transfers = list(result) if result else []
        return TokenTransfersResponse(transfers=transfers, next_page_token="")
