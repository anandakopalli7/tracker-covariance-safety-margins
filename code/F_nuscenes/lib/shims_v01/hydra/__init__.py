"""LOCAL STAND-IN for `hydra` (not installed on this laptop). Import-only: the tracker path never calls hydra; two
CANMOT data-preparation scripts that are imported as a side effect of `canmot.data` decorate their main() with it."""
from . import utils  # noqa: F401


def main(*args, **kwargs):
    def deco(f):
        return f
    return deco


def compose(*args, **kwargs):
    raise RuntimeError('stand-in hydra.compose was actually used')


def initialize_config_dir(*args, **kwargs):
    raise RuntimeError('stand-in hydra.initialize_config_dir was actually used')
