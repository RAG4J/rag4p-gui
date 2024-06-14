import streamlit as st

from rag4p_gui.integrations.opensearch.connect import get_opensearch_access

KEY_SELECTED_OPENSEARCH_COLLECTION = 'selected_opensearch_collection'
LKEY_SELECTED_OPENSEARCH_COLLECTION = '_' + KEY_SELECTED_OPENSEARCH_COLLECTION


def change_opensearch_collection():
    st.session_state[KEY_SELECTED_OPENSEARCH_COLLECTION] = st.session_state.get(LKEY_SELECTED_OPENSEARCH_COLLECTION)


def create_opensearch_collection_selection():
    collections = _obtain_alias_names()

    if not collections:
        st.info('No indexes found in Weaviate')
        return

    if LKEY_SELECTED_OPENSEARCH_COLLECTION in st.session_state:
        index = collections.index(st.session_state.get(LKEY_SELECTED_OPENSEARCH_COLLECTION))
    elif KEY_SELECTED_OPENSEARCH_COLLECTION in st.session_state:
        index = collections.index(st.session_state.get(KEY_SELECTED_OPENSEARCH_COLLECTION))
    else:
        index = 0

    with (st.container(border=True)):
        st.selectbox('Select an existing Opensearch collection',
                     options=collections,
                     key=LKEY_SELECTED_OPENSEARCH_COLLECTION,
                     index=index)

        if st.button("Load Opensearch collection"):
            change_opensearch_collection()


def _obtain_alias_names():
    # Get all aliases
    response = get_opensearch_access().client().indices.get_alias()

    # Extract only the alias names
    alias_names = []
    for index, settings in response.items():
        if index.startswith('.'):
            continue
        aliases = settings.get('aliases', {})
        alias_names.extend(aliases.keys())

    return alias_names