import os

import pytest
from dotenv import load_dotenv
from mm_web3 import fetch_proxies_sync
from typer.testing import CliRunner

load_dotenv()


@pytest.fixture()
def mnemonic() -> str:
    return "hub blur cliff taste afraid master game milk nest change blame code"


@pytest.fixture
def passphrase() -> str:
    return "my-secret"


@pytest.fixture()
def mainnet_bip44_address_0() -> str:
    return "1Men3kiujJH7H5NXyKpFtWWtni1cTfSk48"


@pytest.fixture
def binance_address() -> str:
    return "34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo"


@pytest.fixture()
def proxies_url() -> str:
    res = os.getenv("PROXIES_URL")
    if not res:
        raise ValueError("PROXIES_URL env var is not set")
    return res


@pytest.fixture
def proxies(proxies_url) -> list[str]:
    return fetch_proxies_sync(proxies_url).unwrap("cannot fetch proxies")


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner()
