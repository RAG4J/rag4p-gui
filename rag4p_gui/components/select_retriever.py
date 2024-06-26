import streamlit as st

from rag4p_gui.components.select_content_store import KEY_SELECTED_CONTENT_STORE
from rag4p_gui.components.select_opensearch_collection import KEY_SELECTED_OPENSEARCH_COLLECTION
from rag4p_gui.components.select_weaviate_collection import KEY_SELECTED_WEAVIATE_COLLECTION

KEY_CHOSEN_RETRIEVER = 'chosen_retriever'
VALUE_CHOSEN_RETRIEVER_INTERNAL = 'internal'
VALUE_CHOSEN_RETRIEVER_WEAVIATE = 'weaviate'
VALUE_CHOSEN_RETRIEVER_OPENSEARCH = 'opensearch'

KEY_HYBRID_SEARCH = 'hybrid_search'
LKEY_HYBRID_SEARCH = '_' + KEY_HYBRID_SEARCH


def change_hybrid_search():
    st.session_state[KEY_HYBRID_SEARCH] = st.session_state[LKEY_HYBRID_SEARCH]


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

    if KEY_SELECTED_OPENSEARCH_COLLECTION in st.session_state:
        captions.append(st.session_state.get(KEY_SELECTED_OPENSEARCH_COLLECTION))
        labels.append('OpenSearch')
        values.append(VALUE_CHOSEN_RETRIEVER_OPENSEARCH)

    if KEY_CHOSEN_RETRIEVER in st.session_state:
        index = values.index(st.session_state.get(KEY_CHOSEN_RETRIEVER))
    else:
        index = 0

    if LKEY_HYBRID_SEARCH not in st.session_state:
        st.session_state[LKEY_HYBRID_SEARCH] = st.session_state[KEY_HYBRID_SEARCH]

    with container:
        retriever = st.radio('Choose the retriever', options=labels, captions=captions, index=index)
        if retriever == 'Content Store':
            st.session_state[KEY_CHOSEN_RETRIEVER] = VALUE_CHOSEN_RETRIEVER_INTERNAL
        elif retriever == 'Weaviate':
            st.session_state[KEY_CHOSEN_RETRIEVER] = VALUE_CHOSEN_RETRIEVER_WEAVIATE
        elif retriever == 'OpenSearch':
            st.session_state[KEY_CHOSEN_RETRIEVER] = VALUE_CHOSEN_RETRIEVER_OPENSEARCH

        if retriever != 'Content Store':
            st.toggle(label='Use Hybrid search', key=LKEY_HYBRID_SEARCH, on_change=change_hybrid_search)
