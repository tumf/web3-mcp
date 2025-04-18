# Web3 MCP

[![Tests](https://github.com/tumf/web3-mcp/actions/workflows/test.yml/badge.svg)](https://github.com/tumf/web3-mcp/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/tumf/web3-mcp/branch/main/graph/badge.svg)](https://codecov.io/gh/tumf/web3-mcp)
[![PyPI version](https://badge.fury.io/py/web3-mcp.svg)](https://badge.fury.io/py/web3-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An MCP server implementation wrapping Ankr Advanced API.

## Overview

FastMCP is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that provides access to Ankr's Advanced API for blockchain data. It allows LLMs to interact with blockchain data across multiple chains including Ethereum, BSC, Polygon, Avalanche, and more.

## MCP Client Setting

```json
{
  "mcpServers": {
    "web3": {
      "command": "uvx",
      "args": [
        "web3-mcp"
      ],
      "env": {
        "ANKR_ENDPOINT": "https://rpc.ankr.com/...",
      }
    }
  }
}
```

## Features

- Complete wrapper for all Ankr Advanced API endpoints
- NFT API: Get NFT metadata, holders, transfers, and ownership information
- Query API: Access blockchain statistics, blocks, logs, and transaction data
- Token API: Get token balances, prices, holders, and transfer history
- Support for multiple blockchain networks

## Installation

```bash
# Clone the repository
git clone https://github.com/tumf/web3-mcp.git
cd web3-mcp

# Install with uv
uv pip install -e .
```

## Configuration

Set the following environment variables:

```bash
# Required
export ANKR_ENDPOINT="your_ankr_rpc_endpoint"

# Optional but recommended for authenticated requests
export ANKR_PRIVATE_KEY="your_private_key"
```

## Usage

### Running the server

```python
from web3_mcp.server import init_server

# Initialize MCP server
mcp = init_server(
    name="Ankr MCP",
    endpoint="your_ankr_endpoint",  # Optional, defaults to ANKR_ENDPOINT env var
    private_key="your_private_key"  # Optional, defaults to ANKR_PRIVATE_KEY env var
)

# Run server
mcp.run()
```

### Using with FastMCP CLI

```bash
# Set environment variables first
export ANKR_ENDPOINT="your_ankr_endpoint"
export ANKR_PRIVATE_KEY="your_private_key"

# Run the server
python -m web3_mcp
```

## API Categories

### NFT API

- `get_nfts_by_owner`: Get NFTs owned by a wallet address
- `get_nft_metadata`: Get metadata for a specific NFT
- `get_nft_holders`: Get holders of a specific NFT collection
- `get_nft_transfers`: Get transfer history for NFTs

### Query API

- `get_blockchain_stats`: Get blockchain statistics
- `get_blocks`: Get blocks information
- `get_logs`: Get blockchain logs
- `get_transactions_by_hash`: Get transactions by hash
- `get_transactions_by_address`: Get transactions by address
- `get_interactions`: Get wallet interactions with contracts

### Token API

- `get_account_balance`: Get token balances for a wallet
- `get_currencies`: Get available currencies
- `get_token_price`: Get token price information
- `get_token_holders`: Get token holders
- `get_token_holders_count`: Get token holders count
- `get_token_transfers`: Get token transfer history

## License

MIT
