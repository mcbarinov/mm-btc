from typing import Annotated

import typer
from mm_std import print_plain

from mm_btc.cli import cli_utils
from mm_btc.cli.cmd import mnemonic_cmd

app = typer.Typer(no_args_is_help=True, pretty_exceptions_enable=False, add_completion=False)


@app.command(name="mnemonic", help="Generate keys based on a mnemonic")
def mnemonic_command(  # nosec B107:hardcoded_password_default
    mnemonic: Annotated[str, typer.Option("--mnemonic", "-m", help="")] = "",
    passphrase: Annotated[str, typer.Option("--passphrase", "-pass")] = "",
    path: Annotated[str, typer.Option("--path", help="Derivation path. Examples: bip44, bip88, m/44'/0'/0'/0")] = "bip44",
    words: int = typer.Option(12, "--words", "-w", help="Number of mnemonic words"),
    limit: int = typer.Option(10, "--limit", "-l"),
    testnet: bool = typer.Option(False, "--testnet", "-t", help="Testnet network"),
) -> None:
    mnemonic_cmd.run(
        mnemonic_cmd.Args(
            mnemonic=mnemonic,
            passphrase=passphrase,
            words=words,
            limit=limit,
            path=path,
            testnet=testnet,
        )
    )


def version_callback(value: bool) -> None:
    if value:
        print_plain(f"mm-eth version: {cli_utils.get_version()}")
        raise typer.Exit()


@app.callback()
def main(_version: bool = typer.Option(None, "--version", callback=version_callback, is_eager=True)) -> None:
    pass


if __name__ == "__main_":
    app()
