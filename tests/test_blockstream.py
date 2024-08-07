from mm_btc import blockstream


def test_get_address(binance_address):
    # non-empty address
    res = blockstream.get_address(binance_address)
    assert res.unwrap().chain_stats.tx_count > 800

    # empty address
    res = blockstream.get_address("bc1pa48c294qk7yd7sc8y0wxydc3a2frv5j83e65rvm48v3ej098s5zs8kvh6d")
    assert res.unwrap().chain_stats.tx_count == 0

    # invalid address
    res = blockstream.get_address("bc1pa48c294qk7yd7sc8y0wxydc3a2frv5j83e65rvm48v3ej098s5zs8kvh5d")
    assert res.unwrap_err() == blockstream.ERROR_INVALID_ADDRESS

    # invalid network
    res = blockstream.get_address(binance_address, testnet=True)
    assert res.unwrap_err() == blockstream.ERROR_INVALID_NETWORK


def test_get_confirmed_balance(binance_address):
    res = blockstream.get_confirmed_balance(binance_address)
    assert res.unwrap() > 0
