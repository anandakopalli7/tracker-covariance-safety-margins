"""LOCAL STAND-IN for `hydra.utils` (import-only)."""
import os


def to_absolute_path(path):
    return os.path.abspath(path)
