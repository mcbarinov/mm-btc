from mm_std import print_json

from mm_btc import blockstream
from mm_btc.wallet import is_testnet_address


def run(address: str) -> None:
    testnet = is_testnet_address(address)
    res = blockstream.get_address(address, testnet=testnet)
    print_json(res)
