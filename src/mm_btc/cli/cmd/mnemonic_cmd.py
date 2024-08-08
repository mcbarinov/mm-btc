from dataclasses import dataclass

from mm_std import print_plain

from mm_btc.wallet import derive_accounts, generate_mnemonic


@dataclass
class Args:
    mnemonic: str
    passphrase: str
    words: int
    limit: int
    path: str
    testnet: bool


def run(args: Args) -> None:
    mnemonic = args.mnemonic or generate_mnemonic()
    passphrase = args.passphrase
    path = get_derivation_path_prefix(args.path, args.testnet)
    accounts = derive_accounts(mnemonic, passphrase, path, args.limit)

    print_plain(f"mnemonic: {mnemonic}")
    print_plain(f"passphrase: {passphrase}")
    for acc in accounts:
        print_plain(f"{acc.path} {acc.address} {acc.private}")


def get_derivation_path_prefix(path: str, testnet: bool) -> str:
    if path.startswith("m/"):
        return path
    coin = "1" if testnet else "0"
    if path == "bip44":
        return f"m/44'/{coin}'/0'/0"
    if path == "bip84":
        return f"m/84'/{coin}'/0'/0"

    raise ValueError("Invalid path")
