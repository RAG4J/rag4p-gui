import os
import pytz
from abc import ABC, abstractmethod
from datetime import datetime

import streamlit as st

from rag4p_gui.data.content_store_metadata import ContentStoreMetadata
from rag4p_gui.data.content_store_metadata_service import ContentStoreMetadataService
from rag4p_gui.data.readers.teqnation_jsonl_reader import TeqnationJsonlReader
from rag4p_gui.data.readers.wordpress_jsonl_reader import WordpressJsonlReader
from rag4p_gui.data.readers.dev_to_jsonl_reader import DevToJsonlReader
from rag4p_gui.integrations.weaviate import luminis, teqnation, dev_to
from rag4p_gui.util.embedding import create_embedder
from rag4p_gui.util.splitter import create_splitter

from rag4p.indexing.splitters.max_token_splitter import MaxTokenSplitter
from rag4p.rag.store.content_store import ContentStore
from rag4p.indexing.indexing_service import IndexingService


class IndexingData(ABC):
    def __init__(self, metadata_service: ContentStoreMetadataService):
        self.metadata_service = metadata_service

    def __call__(self, *args, **kwargs):
        state =st.session_state
        self.dataset = st.session_state.selected_data_file

        kwargs = {
            'provider': st.session_state.selected_embedder.lower(),
        }
        kwargs.update(**self.dataset)
        if st.session_state.selected_splitter == MaxTokenSplitter.name():
            kwargs['chunk_size'] = st.session_state.chunk_size

        kwargs['embedding_model'] = st.session_state.selected_embedding_model

        self._create_reader()

        self.collection_name = st.session_state.new_collection_name
        self.embedder = create_embedder(embedder_name=st.session_state.selected_embedder,
                                        model_name=st.session_state.selected_embedding_model)
        self.splitter = create_splitter(splitter_name=st.session_state.selected_splitter, **kwargs)

        content_store = self._create_content_store()

        indexing_service = IndexingService(content_store=content_store)
        response = indexing_service.index_documents(content_reader=self.reader, splitter=self.splitter)

        created_at = datetime.now().replace(tzinfo=pytz.UTC).isoformat()
        content_store_metadata = ContentStoreMetadata(
            collection_name=state.new_collection_name,
            splitter=state.selected_splitter,
            embedder=state.selected_embedder,
            embedding_model=state.selected_embedding_model,
            dataset=state.selected_data_file['name'],
            contentReader=state.selected_data_file['reader'],
            chunk_size=state.chunk_size if state.selected_splitter == MaxTokenSplitter.name() else None,
            num_documents=response.num_documents,
            num_chunks=response.num_chunks,
            running_time=response.running_time,
            created_at=created_at
        )

        self.metadata_service.save_meta_data(content_store_metadata)

        self._after_indexing()

    @abstractmethod
    def _create_content_store(self) -> ContentStore:
        pass

    @abstractmethod
    def _after_indexing(self):
        pass

    def _create_reader(self):
        dataset = self.dataset
        data_path = str(os.path.join(dataset['path'], dataset['file']))
        if dataset['reader'] == WordpressJsonlReader.__name__:
            reader = WordpressJsonlReader(file_name=data_path)
            additional_properties = luminis.additional_properties
        elif dataset['reader'] == TeqnationJsonlReader.__name__:
            reader = TeqnationJsonlReader(file_name=data_path)
            additional_properties = teqnation.additional_properties
        elif dataset['reader'] == DevToJsonlReader.__name__:
            reader = DevToJsonlReader(file_name=data_path)
            additional_properties = dev_to.additional_properties
        else:
            raise ValueError(f"Unknown reader {dataset['reader']}")

        self.reader = reader
        self.additional_properties = additional_properties
