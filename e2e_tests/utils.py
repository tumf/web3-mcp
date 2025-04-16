"""
Test utilities
"""

import asyncio
from typing import Any

import aiohttp


async def make_request_with_retry(
    client: Any, tool_name: str, params: dict, max_retries: int = 3, timeout: int = 10
) -> Any:
    """Make a request with retry logic"""
    for _ in range(max_retries):
        try:
            return await asyncio.wait_for(
                client.call_tool(tool_name, params),
                timeout=timeout,
            )
        except (asyncio.TimeoutError, aiohttp.ClientError) as e:
            if _ == max_retries - 1:
                raise e
            await asyncio.sleep(1)  # Wait before retrying
