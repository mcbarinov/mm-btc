import importlib.metadata
import sys
from pathlib import Path

from mm_std import BaseConfig
from rich import print_json


def get_version() -> str:
    return importlib.metadata.version("mm-btc")


def read_config[T: BaseConfig](config_type: type[T], config_path: Path) -> T:
    res = config_type.read_config(config_path)
    if res.is_ok():
        return res.unwrap()

    print_json(res.err)
    sys.exit(1)
