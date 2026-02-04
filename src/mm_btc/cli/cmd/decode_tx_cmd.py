"""CLI handler for the decode-tx command — decodes a raw transaction hex."""

from mm_print import print_json

from mm_btc.tx import decode_tx


def run(tx_hex: str, testnet: bool = False) -> None:
    """Decode and print a raw Bitcoin transaction."""
    res = decode_tx(tx_hex, testnet)
    print_json(res)
