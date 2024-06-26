import streamlit as st

from rag4p.rag.retrieval.strategies.document_retrieval_strategy import DocumentRetrievalStrategy
from rag4p.rag.retrieval.strategies.topn_retrieval_strategy import TopNRetrievalStrategy
from rag4p.rag.retrieval.strategies.window_retrieval_strategy import WindowRetrievalStrategy
from rag4p.integrations.weaviate.weaviate_retriever import WeaviateRetriever
from rag4p.integrations.openai.openai_embedder import OpenAIEmbedder
from rag4p.integrations.openai import DEFAULT_EMBEDDING_MODEL
from rag4p.integrations.opensearch.opensearch_retriever import OpenSearchRetriever

from rag4p_gui.components.select_content_store import create_content_store_selection, KEY_SELECTED_CONTENT_STORE
from rag4p_gui.components.select_number_of_chunks import create_number_of_chunks_selection, KEY_AMOUNT_OF_CHUNKS
from rag4p_gui.components.select_opensearch_collection import create_opensearch_collection_selection, \
    KEY_SELECTED_OPENSEARCH_COLLECTION
from rag4p_gui.components.select_retriever import KEY_CHOSEN_RETRIEVER, VALUE_CHOSEN_RETRIEVER_INTERNAL, \
    VALUE_CHOSEN_RETRIEVER_WEAVIATE, create_retriever_selection, VALUE_CHOSEN_RETRIEVER_OPENSEARCH, KEY_HYBRID_SEARCH
from rag4p_gui.components.select_strategy import KEY_SELECTED_STRATEGY, LKEY_SELECTED_STRATEGY, \
    create_retrieval_strategy_selection, KEY_WINDOW_SIZE
from rag4p_gui.components.select_weaviate_collection import create_weaviate_collection_selection, \
    KEY_SELECTED_WEAVIATE_COLLECTION
from rag4p_gui.integrations.opensearch.connect import get_opensearch_access
from rag4p_gui.integrations.opensearch.indexing import OpenSearchContentStoreMetadataService
from rag4p_gui.integrations.weaviate.connect import get_weaviate_access
from rag4p_gui.integrations.weaviate.indexing import WeaviateContentStoreMetadataService
from rag4p_gui.util.embedding import create_embedder

LKEY_AMOUNT_OF_CHUNKS = '_' + KEY_AMOUNT_OF_CHUNKS
KEY_RETRIEVAL_STRATEGY = 'retrieval_strategy'


class RetrievalSidebar:

    def __init__(self):
        # Check if we can initialize the retrieval strategy, we need a chosen retriever and a selected strategy
        if (KEY_CHOSEN_RETRIEVER in st.session_state
                and KEY_SELECTED_STRATEGY in st.session_state):
            self.initialize_retrieval_strategy()

    def __call__(self):
        with st.sidebar:
            st.title('Configure')
            chunks_container = st.container(border=True)
            strategy_container = st.container(border=True)
            choose_retriever_container = st.container(border=True)

            create_content_store_selection()
            create_weaviate_collection_selection()
            create_opensearch_collection_selection()

            create_retriever_selection(choose_retriever_container)

            if KEY_CHOSEN_RETRIEVER in st.session_state:
                create_number_of_chunks_selection(chunks_container)
                create_retrieval_strategy_selection(strategy_container)

    @staticmethod
    def initialize_retrieval_strategy():
        hybrid_search = st.session_state[KEY_HYBRID_SEARCH]
        if st.session_state[KEY_CHOSEN_RETRIEVER] == VALUE_CHOSEN_RETRIEVER_INTERNAL:
            content_store = st.session_state.content_store
        elif st.session_state[KEY_CHOSEN_RETRIEVER] == VALUE_CHOSEN_RETRIEVER_WEAVIATE:
            collection_name = st.session_state[KEY_SELECTED_WEAVIATE_COLLECTION]
            service = WeaviateContentStoreMetadataService(get_weaviate_access())
            metadata = service.get_meta_data(collection_name)
            embedder = create_embedder(metadata.embedder, metadata.embedding_model)
            additional_properties = RetrievalSidebar.find_additional_properties_weaviate(collection_name)

            content_store = WeaviateRetriever(get_weaviate_access(),
                                              embedder=embedder,
                                              additional_properties=additional_properties,
                                              hybrid=hybrid_search,
                                              collection_name=collection_name)

        elif st.session_state[KEY_CHOSEN_RETRIEVER] == VALUE_CHOSEN_RETRIEVER_OPENSEARCH:
            index_name = st.session_state[KEY_SELECTED_OPENSEARCH_COLLECTION]
            service = OpenSearchContentStoreMetadataService(get_opensearch_access())
            metadata = service.get_meta_data(index_name)
            embedder = create_embedder(metadata.embedder, metadata.embedding_model)
            additional_properties = RetrievalSidebar.find_additional_properties_opensearch(index_name)

            content_store = OpenSearchRetriever(get_opensearch_access(),
                                                index_name=index_name,
                                                hybrid=hybrid_search,
                                                additional_properties=additional_properties,
                                                embedder=embedder)
        else:
            raise ValueError(f"Unsupported retriever: {st.session_state[KEY_CHOSEN_RETRIEVER]}")

        if st.session_state[KEY_SELECTED_STRATEGY] == TopNRetrievalStrategy.__name__:
            strategy = TopNRetrievalStrategy(retriever=content_store)
        elif st.session_state[KEY_SELECTED_STRATEGY] == WindowRetrievalStrategy.__name__:
            window_size = st.session_state[KEY_WINDOW_SIZE]
            strategy = WindowRetrievalStrategy(retriever=content_store, window_size=window_size)
        elif st.session_state[KEY_SELECTED_STRATEGY] == DocumentRetrievalStrategy.__name__:
            strategy = DocumentRetrievalStrategy(retriever=content_store)
        else:
            raise ValueError(f"Unsupported retrieval strategy: {st.session_state.selected_retrieval_strategy}")
        st.session_state[KEY_RETRIEVAL_STRATEGY] = strategy

    @staticmethod
    def find_additional_properties_weaviate(collection_name: str):
        schema = get_weaviate_access().client.collections.export_config(name=collection_name)
        return [prop.name for prop in schema.properties if prop.index_searchable]

    @staticmethod
    def find_additional_properties_opensearch(index_name: str):
        details = get_opensearch_access().client().indices.get(index=index_name)
        index_name = list(details.keys())[0]
        props = details[index_name]['mappings']['properties']
        return [prop for prop in props if props[prop]['type'] == 'text']
