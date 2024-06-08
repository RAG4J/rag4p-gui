import pandas as pd
import streamlit as st
from rag4p.indexing.splitters.max_token_splitter import MaxTokenSplitter
from rag4p.indexing.splitters.sentence_splitter import SentenceSplitter
from rag4p.indexing.splitters.single_chunk_splitter import SingleChunkSplitter
from rag4p.integrations.ollama import EMBEDDING_MODEL_NOMIC, EMBEDDING_MODEL_MINILM
from rag4p.integrations.ollama.ollama_embedder import OllamaEmbedder
from rag4p.integrations.openai import EMBEDDING_SMALL, EMBEDDING_ADA
from rag4p.integrations.openai.openai_embedder import OpenAIEmbedder
from rag4p.rag.embedding.local.onnx_embedder import OnnxEmbedder
from rag4p.rag.retrieval.strategies.document_retrieval_strategy import DocumentRetrievalStrategy
from rag4p.rag.retrieval.strategies.topn_retrieval_strategy import TopNRetrievalStrategy
from rag4p.rag.retrieval.strategies.window_retrieval_strategy import WindowRetrievalStrategy

from rag4p_gui.components.select_embedder import KEY_AVAILABLE_EMBEDDERS, KEY_SELECTED_EMBEDDER, \
    KEY_SELECTED_EMBEDDING_MODEL
from rag4p_gui.components.select_number_of_chunks import KEY_AMOUNT_OF_CHUNKS
from rag4p_gui.components.select_splitter import KEY_AVAILABLE_SPLITTERS, KEY_SELECTED_SPLITTER, KEY_CHUNK_SIZE
from rag4p_gui.components.select_strategy import KEY_AVAILABLE_STRATEGIES


def init_session():
    # st.write(st.session_state)
    _init_embeddings()
    _init_splitters()

    if KEY_AVAILABLE_STRATEGIES not in st.session_state:
        st.session_state[KEY_AVAILABLE_STRATEGIES] = [
            TopNRetrievalStrategy.__name__,
            WindowRetrievalStrategy.__name__,
            DocumentRetrievalStrategy.__name__
        ]

    if not st.session_state.get('content_store_initialized'):
        st.session_state.content_store_initialized = False

    if KEY_AMOUNT_OF_CHUNKS not in st.session_state:
        st.session_state[KEY_AMOUNT_OF_CHUNKS] = 2


def _init_splitters():
    if KEY_AVAILABLE_SPLITTERS not in st.session_state:
        st.session_state[KEY_AVAILABLE_SPLITTERS] = \
            [SentenceSplitter.name(), MaxTokenSplitter.name(), SingleChunkSplitter.name()]
    if KEY_SELECTED_SPLITTER not in st.session_state:
        st.session_state[KEY_SELECTED_SPLITTER] = st.session_state[KEY_AVAILABLE_SPLITTERS][0]

    if KEY_CHUNK_SIZE not in st.session_state:
        st.session_state[KEY_CHUNK_SIZE] = 512


def _init_embeddings():
    if KEY_AVAILABLE_EMBEDDERS not in st.session_state:
        st.session_state.available_embedders = pd.DataFrame({
            'embedder': [OpenAIEmbedder.supplier(), OllamaEmbedder.supplier(), OnnxEmbedder.supplier()],
            'model': [[EMBEDDING_SMALL, EMBEDDING_ADA], [EMBEDDING_MODEL_NOMIC, EMBEDDING_MODEL_MINILM], ['MiniLM']]
        })
    if KEY_SELECTED_EMBEDDER not in st.session_state:
        st.session_state[KEY_SELECTED_EMBEDDER] = st.session_state.available_embedders['embedder'].values[0]
    if KEY_SELECTED_EMBEDDING_MODEL not in st.session_state:
        current_embedder = st.session_state[KEY_SELECTED_EMBEDDER]
        avail_embedders = st.session_state.available_embedders
        st.session_state[KEY_SELECTED_EMBEDDING_MODEL] = \
            avail_embedders.loc[avail_embedders['embedder'] == current_embedder, 'model'].values[0][0]
