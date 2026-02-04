"""CLI handler for the utxo command — fetches UTXOs from Blockstream."""

from mm_print import print_json

from mm_btc.blockstream import BlockstreamClient
from mm_btc.wallet import is_testnet_address


async def run(address: str) -> None:
    """Fetch and print UTXOs for an address from the Blockstream API."""
    client = BlockstreamClient(testnet=is_testnet_address(address))
    res = await client.get_utxo(address)
    print_json(res.value_or_error())
