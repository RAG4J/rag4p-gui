import streamlit as st
from rag4p.indexing.splitters.max_token_splitter import MaxTokenSplitter

KEY_AVAILABLE_SPLITTERS = 'available_splitters'
KEY_SELECTED_SPLITTER = 'selected_splitter'
KEY_CHUNK_SIZE = 'chunk_size'

LKEY_SELECTED_SPLITTER = '_' + KEY_SELECTED_SPLITTER
LKEY_CHUNK_SIZE = '_' + KEY_CHUNK_SIZE


def store_selected_splitter():
    st.session_state[KEY_SELECTED_SPLITTER] = st.session_state.get(LKEY_SELECTED_SPLITTER)


def store_chunk_size():
    st.session_state[KEY_CHUNK_SIZE] = st.session_state.get(LKEY_CHUNK_SIZE)


def create_splitter_selector(container):
    if LKEY_SELECTED_SPLITTER not in st.session_state:
        if KEY_SELECTED_SPLITTER in st.session_state:
            st.session_state[LKEY_SELECTED_SPLITTER] = st.session_state.get(KEY_SELECTED_SPLITTER)
        else:
            st.session_state[LKEY_SELECTED_SPLITTER] = st.session_state.available_splitters[0]
            st.session_state[KEY_SELECTED_SPLITTER] = st.session_state.available_splitters[0]
    if LKEY_CHUNK_SIZE not in st.session_state:
        if KEY_CHUNK_SIZE in st.session_state:
            st.session_state[LKEY_CHUNK_SIZE] = st.session_state.get(KEY_CHUNK_SIZE)
        else:
            st.session_state[LKEY_CHUNK_SIZE] = 512
            st.session_state[KEY_CHUNK_SIZE] = 512

    with container:
        st.write('Configure the splitter to use for creating chunks.')
        st.selectbox(label='Choose splitter',
                     options=st.session_state[KEY_AVAILABLE_SPLITTERS],
                     key=LKEY_SELECTED_SPLITTER,
                     on_change=store_selected_splitter)
        st.number_input(label='Chunk size',
                        key=LKEY_CHUNK_SIZE,
                        on_change=store_chunk_size,
                        min_value=1,
                        step=1,
                        disabled=st.session_state[LKEY_SELECTED_SPLITTER] != MaxTokenSplitter.name())