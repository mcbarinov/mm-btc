"""Bitcoin transaction decoding utilities."""

from bitcoinlib.transactions import Transaction


def decode_tx(tx_hex: str, testnet: bool = False) -> dict[str, object]:
    """Decode a raw Bitcoin transaction hex string into a dictionary."""
    return Transaction.parse(tx_hex, network="testnet" if testnet else "mainnet").as_dict()  # type: ignore[no-any-return]  # ty: ignore[unused-ignore-comment]  # bitcoinlib has no type stubs, as_dict() returns Any
