import streamlit as st
from rag4p.indexing.splitters.max_token_splitter import MaxTokenSplitter

KEY_AVAILABLE_SPLITTERS = 'available_splitters'
KEY_SELECTED_SPLITTER = 'selected_splitter'
KEY_CHUNK_SIZE = 'chunk_size'

LKEY_SELECTED_SPLITTER = '_' + KEY_SELECTED_SPLITTER
LKEY_CHUNK_SIZE = '_' + KEY_CHUNK_SIZE


def store_selected_splitter():
    st.session_state[KEY_SELECTED_SPLITTER] = st.session_state.get(LKEY_SELECTED_SPLITTER)
    if st.session_state[LKEY_SELECTED_SPLITTER] == MaxTokenSplitter.name():
        st.session_state[KEY_CHUNK_SIZE] = st.session_state.get(LKEY_CHUNK_SIZE)


def create_splitter_selector(container):
    available_splitters = st.session_state[KEY_AVAILABLE_SPLITTERS]
    if LKEY_SELECTED_SPLITTER not in st.session_state:
        splitter_index = available_splitters.index(st.session_state.get(KEY_SELECTED_SPLITTER))
    else:
        splitter_index = available_splitters.index(st.session_state.get(LKEY_SELECTED_SPLITTER))

    if LKEY_CHUNK_SIZE not in st.session_state:
        splitter_token_size = st.session_state.get(KEY_CHUNK_SIZE)
    else:
        splitter_token_size = st.session_state.get(LKEY_CHUNK_SIZE)

    with container:
        st.write('Configure the splitter to use for creating chunks.')
        st.selectbox(label='Choose splitter',
                     options=st.session_state[KEY_AVAILABLE_SPLITTERS],
                     index=splitter_index,
                     key=LKEY_SELECTED_SPLITTER)
        st.number_input(label='Chunk size',
                        key=LKEY_CHUNK_SIZE,
                        min_value=1,
                        step=1,
                        value=splitter_token_size,
                        disabled=st.session_state[LKEY_SELECTED_SPLITTER] != MaxTokenSplitter.name())
        if st.button('Choose splitter'):
            store_selected_splitter()
