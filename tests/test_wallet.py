from mm_btc.wallet import (
    BIP44_MAINNET_PATH,
    BIP44_TESTNET_PATH,
    BIP84_MAINNET_PATH,
    BIP84_TESTNET_PATH,
    derive_accounts,
    generate_mnemonic,
)


def test_generate_mnemonic():
    mnemonic = generate_mnemonic(strength=256)
    assert len(mnemonic.split()) == 24

    assert generate_mnemonic() != generate_mnemonic()


def test_derive_accounts():
    mnemonic = "arrange mutual earth tackle smart kangaroo rigid census exotic acoustic stock dream eager area laptop"
    passphrase = "my-secret"

    # mainnet bip44
    accs = derive_accounts(mnemonic, passphrase, BIP44_MAINNET_PATH, 2)
    assert accs[1].path == "m/44'/0'/0'/0/1"
    assert accs[1].address == "1L4Ghh4kuJuRCXrFrczwCV2TaggfCgf6B3"
    assert accs[1].private == "Kz4zoYPJ5astywoTbxHQr5SgFvMCekMqnWDFnXjY9CfvFtyNnGiE"

    # mainnet bip84
    accs = derive_accounts(mnemonic, passphrase, BIP84_MAINNET_PATH, 2)
    assert accs[1].path == "m/84'/0'/0'/0/1"
    assert accs[1].address == "bc1qrq2mwuqz3utyqz97xjq5npl0dyq5gmddpxdf8k"
    assert accs[1].private == "L447sW2JenqmEMMi7GoiUZDxTpY3Ni5ZfRrRxAbufiYwZV1AHytj"

    # testnet bip44
    accs = derive_accounts(mnemonic, passphrase, BIP44_TESTNET_PATH, 2)
    assert accs[1].path == "m/44'/1'/0'/0/1"
    assert accs[1].address == "n3DsvbopmKJaxHNgdZ6VVK4mB9fcuhXy5w"
    assert accs[1].private == "cVsAhYpSm2x8V2fQJdjmfBGm1aW7xKH1U8eZTpG9giz8usxNv4da"

    # testnet bip84
    accs = derive_accounts(mnemonic, passphrase, BIP84_TESTNET_PATH, 2)
    assert accs[1].path == "m/84'/1'/0'/0/1"
    assert accs[1].address == "tb1q4cu7pgs0w5s4ctjz4m6gx6m4rv8eqjwtnt0a4j"
    assert accs[1].private == "cPASMrozgCxXD6GQsJhge7hPY81j3huF8RJBY1PYwKmUVSYgeSRw"
