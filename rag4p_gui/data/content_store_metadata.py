import datetime
from dataclasses import dataclass


@dataclass
class ContentStoreMetadata:
    collection_name: str
    splitter: str
    chunk_size: int
    embedder: str
    embedding_model: str
    dataset: str
    num_documents: int
    num_chunks: int
    running_time: float
    created_at: datetime
    contentReader: str
