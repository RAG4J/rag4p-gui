import streamlit as st

from rag4p_gui.components.select_content_store import KEY_SELECTED_CONTENT_STORE
from rag4p_gui.components.select_weaviate_collection import KEY_SELECTED_WEAVIATE_COLLECTION

KEY_CHOSEN_RETRIEVER = 'chosen_retriever'
VALUE_CHOSEN_RETRIEVER_INTERNAL = 'internal'
VALUE_CHOSEN_RETRIEVER_WEAVIATE = 'weaviate'


def create_retriever_selection(container):
    labels = []
    captions = []
    values = []
    if KEY_SELECTED_CONTENT_STORE in st.session_state:
        captions.append(st.session_state.get(KEY_SELECTED_CONTENT_STORE))
        labels.append('Content Store')
        values.append(VALUE_CHOSEN_RETRIEVER_INTERNAL)

    if KEY_SELECTED_WEAVIATE_COLLECTION in st.session_state:
        captions.append(st.session_state.get(KEY_SELECTED_WEAVIATE_COLLECTION))
        labels.append('Weaviate')
        values.append(VALUE_CHOSEN_RETRIEVER_WEAVIATE)

    if KEY_CHOSEN_RETRIEVER in st.session_state:
        index = values.index(st.session_state.get(KEY_CHOSEN_RETRIEVER))
    else:
        index = 0

    with container:
        retriever = st.radio('Choose the retriever', options=labels, captions=captions, index=index)
        if retriever == 'Content Store':
            st.session_state[KEY_CHOSEN_RETRIEVER] = VALUE_CHOSEN_RETRIEVER_INTERNAL
        elif retriever == 'Weaviate':
            st.session_state[KEY_CHOSEN_RETRIEVER] = VALUE_CHOSEN_RETRIEVER_WEAVIATE
