from pathlib import Path
from dataclasses import dataclass


@dataclass
class Document:
    path: Path
    name : str
    hash_code : str
    size : int
    text : str = ""

@dataclass
class Chunk:
    text : str
    index : int
    document_hash : str

@dataclass
class Embedding:
    vector: list[float]
    dimension: int

@dataclass
class VectorRecord:
    chunk: Chunk
    embedding: Embedding

@dataclass
class SearchResult:
    chunk: Chunk
    distance: float

@dataclass
class Answer:
    text: str
    references: list[SearchResult]