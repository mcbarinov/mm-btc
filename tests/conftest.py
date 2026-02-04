"""Shared test fixtures."""

import os

import pytest
from dotenv import load_dotenv
from mm_web3 import fetch_proxies_sync
from typer.testing import CliRunner

load_dotenv()


@pytest.fixture()
def mnemonic() -> str:
    """Return a test mnemonic phrase."""
    return "hub blur cliff taste afraid master game milk nest change blame code"


@pytest.fixture
def passphrase() -> str:
    """Return a test passphrase."""
    return "my-secret"


@pytest.fixture()
def mainnet_bip44_address_0() -> str:
    """Return a known mainnet BIP44 address at index 0."""
    return "1Men3kiujJH7H5NXyKpFtWWtni1cTfSk48"


@pytest.fixture
def binance_address() -> str:
    """Return a known Binance address."""
    return "34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo"


@pytest.fixture()
def proxies_url() -> str:
    """Return proxies URL from environment."""
    res = os.getenv("PROXIES_URL")
    if not res:
        raise ValueError("PROXIES_URL env var is not set")
    return res


@pytest.fixture
def proxies(proxies_url) -> list[str]:
    """Fetch and return proxy list."""
    return fetch_proxies_sync(proxies_url).unwrap("cannot fetch proxies")


@pytest.fixture
def cli_runner() -> CliRunner:
    """Return a typer CLI test runner."""
    return CliRunner()
