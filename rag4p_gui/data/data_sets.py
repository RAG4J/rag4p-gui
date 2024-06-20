import asyncio
import json
import os
from os import listdir

from rag4p.indexing.content_reader import ContentReader
from rag4p.indexing.indexing_service import IndexingService
from rag4p.integrations.ollama.ollama_embedder import OllamaEmbedder
from rag4p.integrations.ollama import EMBEDDING_MODEL_NOMIC, EMBEDDING_MODEL_MINILM
from rag4p.integrations.openai import EMBEDDING_SMALL
from rag4p.integrations.openai.openai_embedder import OpenAIEmbedder
from rag4p.rag.store.local.internal_content_store import InternalContentStore

from rag4p_gui.data.readers.wordpress_jsonl_reader import WordpressJsonlReader
from rag4p_gui.util.embedding import create_embedder
from rag4p_gui.util.splitter import create_splitter


async def load_internal_content_store(content_reader: ContentReader, splitter_name: str, embedder_name: str,
                                      embedding_model: str, **kwargs) -> InternalContentStore:
    """
    Create a new ContentStore that is initialized with the provided content reader, embedder and splitter.
    :param content_reader: The content reader to read the content from.
    :param splitter_name: The splitter to split the content into chunks.
    :param embedder_name: The embedder provider using the model provided.
    :param embedding_model: Name of the model to use for the embedder.
    :param kwargs: Additional arguments to pass to be used by one of the provided components.
    :return:
    """
    kwargs['embedding_model'] = embedding_model

    splitter = create_splitter(splitter_name=splitter_name, **kwargs)
    embedder = create_embedder(embedder_name=embedder_name, model_name=embedding_model)
    meta = {
        'splitter': splitter.name(),
    }
    if kwargs:
        meta.update(kwargs)
    internal_content_store = InternalContentStore(embedder=embedder, metadata=meta)
    indexing_service = IndexingService(content_store=internal_content_store)

    indexing_service.index_documents(content_reader=content_reader, splitter=splitter)

    return internal_content_store


def available_content_stores(path: str = "../../data_backups"):
    current_script_path = os.path.dirname(os.path.realpath(__file__))
    combined_path = os.path.join(current_script_path, path)
    normalized_path = os.path.normpath(combined_path)
    return [f.removesuffix('_metadata.json') for f in listdir(normalized_path) if f.endswith(".json")]


def available_data_files(path: str = "../../data"):
    current_script_path = os.path.dirname(os.path.realpath(__file__))
    combined_path = os.path.join(current_script_path, path, "metadata.json")
    normalized_path = os.path.normpath(combined_path)
    # load json document into dictionary
    with open(normalized_path, 'r') as file:
        data = json.load(file)
    return data


def content_store_metadata_from_backup(path: str):
    current_script_path = os.path.dirname(os.path.realpath(__file__))
    combined_path = os.path.join(current_script_path, path)
    normalized_path = os.path.normpath(combined_path)

    with open(f'{normalized_path}_metadata.json', 'r') as f:
        metadata = json.load(f)

    return metadata
