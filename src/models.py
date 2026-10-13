from pathlib import Path
from dataclasses import dataclass


@dataclass
class Document:
    path: Path
    name : str
    hash_code : str
    size : int
    text : str