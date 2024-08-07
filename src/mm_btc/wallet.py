from dataclasses import dataclass

from hdwallet import BIP44HDWallet, BIP84HDWallet
from hdwallet.symbols import BTC, BTCTEST
from hdwallet.utils import generate_mnemonic as new_mnemonic

BIP44_MAINNET_PATH = "m/44'/0'/0'/0"
BIP44_TESTNET_PATH = "m/44'/1'/0'/0"
BIP84_MAINNET_PATH = "m/84'/0'/0'/0"
BIP84_TESTNET_PATH = "m/84'/1'/0'/0"


@dataclass
class Account:
    address: str
    private: str
    path: str


def generate_mnemonic(language: str = "english", strength: int = 128) -> str:
    return new_mnemonic(language=language, strength=strength)  # type: ignore[no-any-return]


def derive_accounts(mnemonic: str, passphrase: str, path: str, limit: int) -> list[Account]:
    if path.startswith("m/84'/1'"):
        w = BIP84HDWallet(symbol=BTCTEST)
    elif path.startswith("m/44'/1'"):
        w = BIP44HDWallet(symbol=BTCTEST)
    elif path.startswith("m/84'/0'"):
        w = BIP84HDWallet(symbol=BTC)
    elif path.startswith("m/44'/0'"):
        w = BIP44HDWallet(symbol=BTC)
    else:
        raise ValueError("Invalid path")

    w.from_mnemonic(mnemonic, passphrase=passphrase)
    w.clean_derivation()

    accounts = []
    for index_path in range(limit):
        w.from_path(path=f"{path}/{index_path}")
        accounts.append(Account(address=w.address(), private=w.wif(), path=f"{path}/{index_path}"))
        w.clean_derivation()

    return accounts
