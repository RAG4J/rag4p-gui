import streamlit as st

from rag4p_gui.integrations.opensearch.connect import get_opensearch_access, NoAwsSessionError
from rag4p_gui.integrations.opensearch.indexing import OpenSearchContentStoreMetadataService

KEY_SELECTED_OPENSEARCH_COLLECTION = 'selected_opensearch_collection'
LKEY_SELECTED_OPENSEARCH_COLLECTION = '_' + KEY_SELECTED_OPENSEARCH_COLLECTION


def create_opensearch_collection_selection():
    collections = _obtain_alias_names()

    if not collections:
        st.info('No indexes found in OpenSearch.')
        return

    if LKEY_SELECTED_OPENSEARCH_COLLECTION in st.session_state:
        index = collections.index(st.session_state.get(LKEY_SELECTED_OPENSEARCH_COLLECTION))
    elif KEY_SELECTED_OPENSEARCH_COLLECTION in st.session_state:
        index = collections.index(st.session_state.get(KEY_SELECTED_OPENSEARCH_COLLECTION))
    else:
        index = 0

    with (st.container(border=True)):
        st.session_state[LKEY_SELECTED_OPENSEARCH_COLLECTION] = st.selectbox('Select an existing Opensearch collection',
                                                                             options=collections,
                                                                             index=index)

        if st.button("Load Opensearch collection"):
            st.session_state[KEY_SELECTED_OPENSEARCH_COLLECTION] = \
                st.session_state.get(LKEY_SELECTED_OPENSEARCH_COLLECTION)


def _obtain_alias_names():
    try:
        service = OpenSearchContentStoreMetadataService(get_opensearch_access())

        available_data = service.get_all_meta_data()
        return [data.collection_name for data in available_data]
    except NoAwsSessionError as e:
        st.error(f"{e}")
        return []