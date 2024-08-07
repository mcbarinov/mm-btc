from collections.abc import Sequence
from typing import TypeAlias

from mm_std import Err, Ok, Result, hr
from mm_std.random_ import random_str_choice
from pydantic import BaseModel

MAINNET_BASE_URL = "https://blockstream.info/api"
TESTNET_BASE_URL = "https://blockstream.info/testnet/api"

ERROR_INVALID_ADDRESS = "INVALID_ADDRESS"
ERROR_INVALID_NETWORK = "INVALID_NETWORK"

Proxy: TypeAlias = str | Sequence[str] | None


class Address(BaseModel):
    class ChainStats(BaseModel):
        funded_txo_count: int
        funded_txo_sum: int
        spent_txo_count: int
        spent_txo_sum: int
        tx_count: int

    class MempoolStats(BaseModel):
        funded_txo_count: int
        funded_txo_sum: int
        spent_txo_count: int
        spent_txo_sum: int
        tx_count: int

    chain_stats: ChainStats
    mempool_stats: MempoolStats


def get_address(
    address: str, testnet: bool = False, timeout: int = 10, proxies: Proxy = None, attempts: int = 1
) -> Result[Address]:
    result: Result[Address] = Err("not started yet")
    data = None
    base_url = TESTNET_BASE_URL if testnet else MAINNET_BASE_URL
    for _ in range(attempts):
        try:
            res = hr(f"{base_url}/address/{address}", timeout=timeout, proxy=random_str_choice(proxies))
            data = res.to_dict()
            if res.code == 400 and (
                "invalid bitcoin address" in res.body.lower() or "bech32 segwit decoding error" in res.body.lower()
            ):
                return Err(ERROR_INVALID_ADDRESS, data=data)
            elif res.code == 400 and "invalid network" in res.body.lower():
                return Err(ERROR_INVALID_NETWORK, data=data)
            return Ok(Address(**res.json))
        except Exception as err:
            result = Err(err, data=data)
    return result


def get_confirmed_balance(
    address: str, testnet: bool = False, timeout: int = 10, proxies: Proxy = None, attempts: int = 1
) -> Result[int]:
    return get_address(address, testnet=testnet, timeout=timeout, proxies=proxies, attempts=attempts).and_then(
        lambda a: Ok(a.chain_stats.funded_txo_sum - a.chain_stats.spent_txo_sum),
    )
