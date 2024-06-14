import os

import streamlit as st

from rag4p.rag.store.local.internal_content_store import InternalContentStore

from rag4p_gui.data.data_sets import available_content_stores, content_store_metadata_from_backup
from rag4p_gui.util.embedding import create_embedder

KEY_SELECTED_CONTENT_STORE = 'selected_content_store'
LKEY_SELECTED_CONTENT_STORE = '_' + KEY_SELECTED_CONTENT_STORE


def load_content_store_from_backup():
    st.session_state[KEY_SELECTED_CONTENT_STORE] = st.session_state[LKEY_SELECTED_CONTENT_STORE]
    backup_path = f"../../data_backups/{st.session_state[KEY_SELECTED_CONTENT_STORE]}"

    current_script_path = os.path.dirname(os.path.realpath(__file__))
    combined_path = os.path.join(current_script_path, backup_path)
    normalized_path = os.path.normpath(combined_path)

    metadata = content_store_metadata_from_backup(backup_path)
    _content_store = InternalContentStore.load_from_backup(
        embedder=create_embedder(embedder_name=metadata['supplier'], model_name=metadata['model']),
        path=normalized_path)
    st.session_state.content_store = _content_store
    st.session_state.content_store_initialized = True


def create_content_store_selection():
    stores = available_content_stores()

    if not stores:
        st.info('No content store backups found')
        return

    if LKEY_SELECTED_CONTENT_STORE in st.session_state:
        index = stores.index(st.session_state.get(LKEY_SELECTED_CONTENT_STORE))
    elif KEY_SELECTED_CONTENT_STORE in st.session_state:
        index = stores.index(st.session_state.get(KEY_SELECTED_CONTENT_STORE))
    else:
        index = 0

    with st.container(border=True):
        st.session_state[LKEY_SELECTED_CONTENT_STORE] = st.selectbox('Select a Content Store backup',
                                                                     options=stores,
                                                                     index=index)

        if st.button("Load Content Store backup"):
            load_content_store_from_backup()
