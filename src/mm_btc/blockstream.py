"""Blockstream Esplora API client for querying Bitcoin blockchain data."""

from collections.abc import Sequence

from mm_http import HttpResponse, http_request
from mm_result import Result
from mm_web3 import random_proxy
from pydantic import BaseModel

# Blockstream API base URLs.
MAINNET_BASE_URL = "https://blockstream.info/api"
TESTNET_BASE_URL = "https://blockstream.info/testnet/api"

# Error constant for HTTP 400 responses.
ERROR_400_BAD_REQUEST = "400 Bad Request"

type Proxy = str | Sequence[str] | None


class Mempool(BaseModel):
    """Bitcoin mempool summary statistics."""

    count: int
    vsize: int
    total_fee: int
    fee_histogram: list[tuple[float, int]]


class Address(BaseModel):
    """Bitcoin address information with on-chain and mempool statistics."""

    class ChainStats(BaseModel):
        """Confirmed on-chain transaction statistics for an address."""

        funded_txo_count: int
        funded_txo_sum: int
        spent_txo_count: int
        spent_txo_sum: int
        tx_count: int

    class MempoolStats(BaseModel):
        """Unconfirmed mempool transaction statistics for an address."""

        funded_txo_count: int
        funded_txo_sum: int
        spent_txo_count: int
        spent_txo_sum: int
        tx_count: int

    chain_stats: ChainStats
    mempool_stats: MempoolStats


class Utxo(BaseModel):
    """Unspent transaction output."""

    class Status(BaseModel):
        """Confirmation status of a UTXO."""

        confirmed: bool
        block_height: int
        block_hash: str
        block_time: int

    txid: str
    vout: int
    status: Status
    value: int


class BlockstreamClient:
    """HTTP client for the Blockstream Esplora REST API."""

    def __init__(self, testnet: bool = False, timeout: float = 5, proxies: Proxy = None, attempts: int = 1) -> None:
        """Initialize the client with network, timeout, proxy, and retry settings."""
        self.testnet = testnet
        self.timeout = timeout
        self.proxies = proxies
        self.attempts = attempts
        self.base_url = TESTNET_BASE_URL if testnet else MAINNET_BASE_URL

    async def get_address(self, address: str) -> Result[Address]:
        """Fetch address information including chain and mempool stats."""
        result: Result[Address] = Result.err("not started yet")
        for _ in range(self.attempts):
            res = await self._request(f"/address/{address}")
            try:
                if res.status_code == 400:
                    return res.to_result_err("400 Bad Request")
                return res.to_result_ok(Address(**res.json_body().unwrap()))
            except Exception as e:
                result = res.to_result_err(e)
        return result

    async def get_confirmed_balance(self, address: str) -> Result[int]:
        """Fetch the confirmed balance (funded minus spent) for an address."""
        return (await self.get_address(address)).chain(
            lambda a: Result.ok(a.chain_stats.funded_txo_sum - a.chain_stats.spent_txo_sum)
        )

    async def get_utxo(self, address: str) -> Result[list[Utxo]]:
        """Fetch the list of UTXOs for an address."""
        result: Result[list[Utxo]] = Result.err("not started yet")
        for _ in range(self.attempts):
            res = await self._request(f"/address/{address}/utxo")
            try:
                return res.to_result_ok([Utxo(**out) for out in res.json_body().unwrap()])
            except Exception as e:
                result = res.to_result_err(e)
        return result

    async def get_mempool(self) -> Result[Mempool]:
        """Fetch current mempool summary statistics."""
        result: Result[Mempool] = Result.err("not started yet")
        for _ in range(self.attempts):
            res = await self._request("/mempool")
            try:
                return res.to_result_ok(Mempool(**res.json_body().unwrap()))
            except Exception as e:
                result = res.to_result_err(e)
        return result

    async def _request(self, url: str) -> HttpResponse:
        """Send an HTTP GET request to the Blockstream API."""
        return await http_request(f"{self.base_url}{url}", timeout=self.timeout, proxy=random_proxy(self.proxies))
