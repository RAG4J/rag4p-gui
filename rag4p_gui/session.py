import streamlit as st
import pandas as pd
from rag4p.integrations.ollama import EMBEDDING_MODEL_NOMIC, EMBEDDING_MODEL_MINILM
from rag4p.integrations.openai import EMBEDDING_SMALL, EMBEDDING_ADA

KEY_AVAILABLE_EMBEDDERS = 'available_embedders'
KEY_SELECTED_EMBEDDER = 'selected_embedder'
KEY_SELECTED_EMBEDDING_MODEL = 'selected_embedding_model'

KEY_SELECTED_SPLITTER = 'selected_splitter'
KEY_CHUNK_SIZE = 'chunk_size'
KEY_AVAILABLE_SPLITTERS = 'available_splitters'


def init_session():
    if KEY_AVAILABLE_EMBEDDERS not in st.session_state:
        st.session_state.available_embedders = pd.DataFrame({
            'embedder': ['OpenAI', 'Ollama', 'Local'],
            'model': [[EMBEDDING_SMALL, EMBEDDING_ADA], [EMBEDDING_MODEL_NOMIC, EMBEDDING_MODEL_MINILM], ['Default']]
        })

    embeddings = st.session_state.available_embedders
    if KEY_SELECTED_EMBEDDER not in st.session_state:
        st.session_state[KEY_SELECTED_EMBEDDER] = embeddings['embedder'][0]
        st.session_state[KEY_SELECTED_EMBEDDING_MODEL] = embeddings['model'][0][0]

    if KEY_AVAILABLE_SPLITTERS not in st.session_state:
        st.session_state.available_splitters = ['sentence', 'max size', 'single chunk']

    if KEY_SELECTED_SPLITTER not in st.session_state:
        st.session_state[KEY_SELECTED_SPLITTER] = 'sentence'
        st.session_state[KEY_CHUNK_SIZE] = 512