import os
from pathlib import Path


def writeable(path_str: str) -> bool:
    path: Path = Path(path_str)

    if path.exists():
        return False

    parent: Path = path.parent
    return parent.exists() and parent.is_dir() and os.access(parent, os.W_OK)
