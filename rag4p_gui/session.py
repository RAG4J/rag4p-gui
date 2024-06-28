import pandas as pd
import streamlit as st
from rag4p.indexing.splitters.max_token_splitter import MaxTokenSplitter
from rag4p.indexing.splitters.sentence_splitter import SentenceSplitter
from rag4p.indexing.splitters.single_chunk_splitter import SingleChunkSplitter
from rag4p.integrations.ollama import EMBEDDING_MODEL_NOMIC, EMBEDDING_MODEL_MINILM, MODEL_PHI3, MODEL_LLAMA3
from rag4p.integrations.ollama.ollama_embedder import OllamaEmbedder
from rag4p.integrations.openai import EMBEDDING_SMALL, EMBEDDING_ADA, MODEL_GPT4O, MODEL_GPT4, MODEL_GPT4_TURBO, \
    MODEL_GPT35_TURBO
from rag4p.integrations.bedrock import MODEL_TITAN_EXPRESS, EMBEDDING_MODEL_TITAN, EMBEDDING_MODEL_TITAN_V2
from rag4p.integrations.bedrock.bedrock_embedder import BedrockEmbedder
from rag4p.integrations.openai.openai_embedder import OpenAIEmbedder
from rag4p.rag.embedding.local.onnx_embedder import OnnxEmbedder
from rag4p.rag.retrieval.strategies.document_retrieval_strategy import DocumentRetrievalStrategy
from rag4p.rag.retrieval.strategies.topn_retrieval_strategy import TopNRetrievalStrategy
from rag4p.rag.retrieval.strategies.window_retrieval_strategy import WindowRetrievalStrategy

from rag4p_gui.components.select_embedder import KEY_AVAILABLE_EMBEDDERS, KEY_SELECTED_EMBEDDER, \
    KEY_SELECTED_EMBEDDING_MODEL
from rag4p_gui.components.select_llm import KEY_AVAILABLE_LLMS, KEY_SELECTED_LLM_PROVIDER, KEY_SELECTED_LLM_MODEL
from rag4p_gui.components.select_number_of_chunks import KEY_AMOUNT_OF_CHUNKS
from rag4p_gui.components.select_retriever import KEY_HYBRID_SEARCH
from rag4p_gui.components.select_splitter import KEY_AVAILABLE_SPLITTERS, KEY_SELECTED_SPLITTER, KEY_CHUNK_SIZE
from rag4p_gui.components.select_strategy import KEY_AVAILABLE_STRATEGIES


def init_session():
    _init_embeddings()
    _init_splitters()
    _init_llms()
    _init_hybrid_search()

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
            'embedder': [OpenAIEmbedder.supplier(), OllamaEmbedder.supplier(), BedrockEmbedder.supplier(),
                         OnnxEmbedder.supplier()],
            'model': [[EMBEDDING_SMALL, EMBEDDING_ADA], [EMBEDDING_MODEL_NOMIC, EMBEDDING_MODEL_MINILM],
                      [EMBEDDING_MODEL_TITAN_V2, EMBEDDING_MODEL_TITAN], ['MiniLM']]
        })
    if KEY_SELECTED_EMBEDDER not in st.session_state:
        st.session_state[KEY_SELECTED_EMBEDDER] = st.session_state.available_embedders['embedder'].values[0]
    if KEY_SELECTED_EMBEDDING_MODEL not in st.session_state:
        current_embedder = st.session_state[KEY_SELECTED_EMBEDDER]
        avail_embedders = st.session_state.available_embedders
        st.session_state[KEY_SELECTED_EMBEDDING_MODEL] = \
            avail_embedders.loc[avail_embedders['embedder'] == current_embedder, 'model'].values[0][0]


def _init_llms():
    if KEY_AVAILABLE_LLMS not in st.session_state:
        st.session_state[KEY_AVAILABLE_LLMS] = pd.DataFrame({
            'llm': ['OpenAI', 'Ollama', 'Bedrock'],
            'model': [
                [MODEL_GPT4O, MODEL_GPT4_TURBO, MODEL_GPT4, MODEL_GPT35_TURBO],
                [MODEL_PHI3, MODEL_LLAMA3, "gemma2"],
                [MODEL_TITAN_EXPRESS, "meta.llama3-70b-instruct-v1:0", "anthropic.claude-3-sonnet-20240229-v1:0"]]
        })
    if KEY_SELECTED_LLM_PROVIDER not in st.session_state:
        st.session_state[KEY_SELECTED_LLM_PROVIDER] = st.session_state[KEY_AVAILABLE_LLMS]['llm'].values[0]
    if KEY_SELECTED_LLM_MODEL not in st.session_state:
        current_llm = st.session_state[KEY_SELECTED_LLM_PROVIDER]
        avail_llms = st.session_state[KEY_AVAILABLE_LLMS]
        st.session_state[KEY_SELECTED_LLM_MODEL] = \
            avail_llms.loc[avail_llms['llm'] == current_llm, 'model'].values[0][0]


def _init_hybrid_search():
    if KEY_HYBRID_SEARCH not in st.session_state:
        st.session_state[KEY_HYBRID_SEARCH] = True
