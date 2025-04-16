"""
Constants for Ankr API integration
"""

NFT_GET_BY_OWNER = "ankr_getNFTsByOwner"
NFT_GET_METADATA = "ankr_getNFTMetadata"
NFT_GET_HOLDERS = "ankr_getNFTHolders"
NFT_GET_TRANSFERS = "ankr_getNftTransfers"

QUERY_GET_BLOCKCHAIN_STATS = "ankr_getBlockchainStats"
QUERY_GET_BLOCKS = "ankr_getBlocks"
QUERY_GET_LOGS = "ankr_getLogs"
QUERY_GET_TRANSACTIONS_BY_HASH = "ankr_getTransactionsByHash"
QUERY_GET_TRANSACTIONS_BY_ADDRESS = "ankr_getTransactionsByAddress"
QUERY_GET_INTERACTIONS = "ankr_getInteractions"

TOKEN_GET_ACCOUNT_BALANCE = "ankr_getAccountBalance"
TOKEN_GET_CURRENCIES = "ankr_getCurrencies"
TOKEN_GET_TOKEN_PRICE = "ankr_getTokenPrice"
TOKEN_GET_TOKEN_HOLDERS = "ankr_getTokenHolders"
TOKEN_GET_TOKEN_HOLDERS_COUNT = "ankr_getTokenHoldersCount"
TOKEN_GET_TOKEN_TRANSFERS = "ankr_getTokenTransfers"

SUPPORTED_NETWORKS = [
    "eth", "bsc", "polygon", "avalanche", "arbitrum", "fantom", "optimism"
]
