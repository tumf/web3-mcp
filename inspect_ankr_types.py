"""
Script to inspect Ankr SDK request types and their parameters
"""
import inspect
from ankr.types import (
    GetNFTsByOwnerRequest,
    GetNFTMetadataRequest,
    GetBlockchainStatsRequest,
    GetBlocksRequest,
    GetAccountBalanceRequest,
    GetTokenPriceRequest
)

def print_class_params(cls):
    """Print the parameters for a class constructor"""
    print(f"\n{cls.__name__} parameters:")
    sig = inspect.signature(cls.__init__)
    for param_name, param in sig.parameters.items():
        if param_name != 'self':
            print(f"  - {param_name}: {param.default if param.default is not inspect.Parameter.empty else 'REQUIRED'}")

print_class_params(GetNFTsByOwnerRequest)
print_class_params(GetNFTMetadataRequest)

print_class_params(GetBlockchainStatsRequest)
print_class_params(GetBlocksRequest)

print_class_params(GetAccountBalanceRequest)
print_class_params(GetTokenPriceRequest)
