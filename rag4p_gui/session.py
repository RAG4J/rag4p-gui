import streamlit as st
import pandas as pd
from rag4p.integrations.ollama import EMBEDDING_MODEL_NOMIC, EMBEDDING_MODEL_MINILM
from rag4p.integrations.ollama.ollama_embedder import OllamaEmbedder
from rag4p.integrations.openai import EMBEDDING_SMALL, EMBEDDING_ADA
from rag4p.integrations.openai.openai_embedder import OpenAIEmbedder
from rag4p.rag.embedding.local.onnx_embedder import OnnxEmbedder
from rag4p.indexing.splitters.max_token_splitter import MaxTokenSplitter
from rag4p.indexing.splitters.sentence_splitter import SentenceSplitter
from rag4p.indexing.splitters.single_chunk_splitter import SingleChunkSplitter
from rag4p.rag.retrieval.strategies.topn_retrieval_strategy import TopNRetrievalStrategy
from rag4p.rag.retrieval.strategies.window_retrieval_strategy import WindowRetrievalStrategy
from rag4p.rag.retrieval.strategies.document_retrieval_strategy import DocumentRetrievalStrategy

KEY_AVAILABLE_EMBEDDERS = 'available_embedders'
KEY_SELECTED_EMBEDDER = 'selected_embedder'
KEY_SELECTED_EMBEDDING_MODEL = 'selected_embedding_model'

KEY_SELECTED_SPLITTER = 'selected_splitter'
KEY_CHUNK_SIZE = 'chunk_size'
KEY_AVAILABLE_SPLITTERS = 'available_splitters'

KEY_AVAILABLE_STRATEGIES = 'available_strategies'
KEY_SELECTED_STRATEGY = 'selected_strategy'
KEY_WINDOW_SIZE = 'window_size'
KEY_AMOUNT_OF_CHUNKS = 'amount_of_chunks'


def init_session():
    if KEY_AVAILABLE_EMBEDDERS not in st.session_state:
        st.session_state.available_embedders = pd.DataFrame({
            'embedder': [OpenAIEmbedder.supplier(), OllamaEmbedder.supplier(), OnnxEmbedder.supplier()],
            'model': [[EMBEDDING_SMALL, EMBEDDING_ADA], [EMBEDDING_MODEL_NOMIC, EMBEDDING_MODEL_MINILM], ['MiniLM']]
        })

    embeddings = st.session_state.available_embedders
    if KEY_SELECTED_EMBEDDER not in st.session_state:
        st.session_state[KEY_SELECTED_EMBEDDER] = embeddings['embedder'][0]
        st.session_state[KEY_SELECTED_EMBEDDING_MODEL] = embeddings['model'][0][0]

    if KEY_AVAILABLE_SPLITTERS not in st.session_state:
        st.session_state.available_splitters = [SentenceSplitter.name(), MaxTokenSplitter.name(),
                                                SingleChunkSplitter.name()]

    if KEY_SELECTED_SPLITTER not in st.session_state:
        st.session_state[KEY_SELECTED_SPLITTER] = st.session_state.available_splitters[0]
        st.session_state[KEY_CHUNK_SIZE] = 512

    if KEY_AVAILABLE_STRATEGIES not in st.session_state:
        st.session_state.available_strategies = [
            TopNRetrievalStrategy.__name__,
            WindowRetrievalStrategy.__name__,
            DocumentRetrievalStrategy.__name__
        ]

    if KEY_SELECTED_STRATEGY not in st.session_state:
        st.session_state[KEY_SELECTED_STRATEGY] = st.session_state.available_strategies[0]
        st.session_state[KEY_WINDOW_SIZE] = 1

    if KEY_AMOUNT_OF_CHUNKS not in st.session_state:
        st.session_state[KEY_AMOUNT_OF_CHUNKS] = 2
