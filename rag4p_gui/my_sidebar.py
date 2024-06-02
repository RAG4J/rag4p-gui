import streamlit as st
import pandas as pd

from rag4p.indexing.splitters.max_token_splitter import MaxTokenSplitter
from rag4p_gui.session import KEY_SELECTED_EMBEDDER, KEY_SELECTED_EMBEDDING_MODEL, KEY_SELECTED_SPLITTER, \
    KEY_CHUNK_SIZE, KEY_AVAILABLE_SPLITTERS

LKEY_SELECTED_EMBEDDER = '_' + KEY_SELECTED_EMBEDDER
LKEY_SELECTED_EMBEDDING_MODEL = '_' + KEY_SELECTED_EMBEDDING_MODEL
LKEY_SELECTED_SPLITTER = '_' + KEY_SELECTED_SPLITTER
LKEY_CHUNK_SIZE = '_' + KEY_CHUNK_SIZE


class MySidebar():

    def __init__(self, embeddings: pd.DataFrame):
        self.embeddings = embeddings
        st.session_state[LKEY_SELECTED_EMBEDDER] = st.session_state[KEY_SELECTED_EMBEDDER]
        st.session_state[LKEY_SELECTED_EMBEDDING_MODEL] = st.session_state[KEY_SELECTED_EMBEDDING_MODEL]
        st.session_state[LKEY_SELECTED_SPLITTER] = st.session_state[KEY_SELECTED_SPLITTER]
        st.session_state[LKEY_CHUNK_SIZE] = st.session_state[KEY_CHUNK_SIZE]

    def store_selected_embedder(self):
        st.session_state[KEY_SELECTED_EMBEDDER] = st.session_state.get(LKEY_SELECTED_EMBEDDER)
        # Update the selected model to use the first model from the selected embedder
        st.session_state[KEY_SELECTED_EMBEDDING_MODEL] = \
            self.embeddings.loc[self.embeddings['embedder'] == st.session_state.selected_embedder, 'model'].values[0][0]

    def store_selected_model(self):
        st.session_state[KEY_SELECTED_EMBEDDING_MODEL] = st.session_state.get(LKEY_SELECTED_EMBEDDING_MODEL)

    def store_selected_splitter(self):
        st.session_state[KEY_SELECTED_SPLITTER] = st.session_state.get(LKEY_SELECTED_SPLITTER)

    def store_chunk_size(self):
        st.session_state[KEY_CHUNK_SIZE] = st.session_state.get(LKEY_CHUNK_SIZE)

    def add_sidebar(self):
        with st.sidebar:
            st.title('Configure')
            with st.container(border=True):
                st.write('Configure the embedding to use. First you choose the provider and then the model.')
                st.selectbox(label='Choose provider',
                             options=self.embeddings['embedder'].tolist(),
                             key=LKEY_SELECTED_EMBEDDER,
                             on_change=self.store_selected_embedder)
                model_options = \
                    self.embeddings.loc[
                        self.embeddings['embedder'] == st.session_state.selected_embedder, 'model'].values[0]
                st.selectbox(label='Choose model',
                             options=model_options,
                             key=LKEY_SELECTED_EMBEDDING_MODEL,
                             on_change=self.store_selected_model)

            with st.container(border=True):
                st.write('Configure the splitter to use for creating chunks.')
                st.selectbox(label='Choose splitter',
                             options=st.session_state[KEY_AVAILABLE_SPLITTERS],
                             key=LKEY_SELECTED_SPLITTER,
                             on_change=self.store_selected_splitter)
                st.number_input(label='Chunk size',
                                key=LKEY_CHUNK_SIZE,
                                on_change=self.store_chunk_size,
                                min_value=1,
                                step=1,
                                disabled=True if st.session_state[LKEY_SELECTED_SPLITTER] != MaxTokenSplitter.name() else False)