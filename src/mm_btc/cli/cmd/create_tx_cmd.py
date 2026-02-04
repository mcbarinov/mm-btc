"""CLI handler for the create-tx command — builds a Bitcoin transaction from a TOML config."""

from pathlib import Path

from bit import PrivateKey, PrivateKeyTestnet
from mm_print import print_json
from mm_web3 import Web3CliConfig

from mm_btc.wallet import is_testnet_address


class Config(Web3CliConfig):
    """Transaction creation configuration loaded from a TOML file."""

    class Output(Web3CliConfig):
        """Single transaction output with destination address and amount in satoshis."""

        address: str
        amount: int

    from_address: str
    private: str
    outputs: list[Output]


def run(config_path: Path) -> None:
    """Build and print a signed Bitcoin transaction from the given config file."""
    config = Config.read_toml_config_or_exit(config_path)
    testnet = is_testnet_address(config.from_address)
    key = PrivateKeyTestnet(config.private) if testnet else PrivateKey(config.private)

    outputs = [(o.address, o.amount, "satoshi") for o in config.outputs]

    tx = key.create_transaction(outputs)
    print_json(tx)
