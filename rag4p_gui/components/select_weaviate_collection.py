import streamlit as st

from rag4p_gui.integrations.weaviate.connect import get_weaviate_access

KEY_SELECTED_WEAVIATE_COLLECTION = 'selected_weaviate_collection'
LKEY_SELECTED_WEAVIATE_COLLECTION = '_' + KEY_SELECTED_WEAVIATE_COLLECTION


def change_weaviate_collection():
    st.session_state[KEY_SELECTED_WEAVIATE_COLLECTION] = st.session_state.get(LKEY_SELECTED_WEAVIATE_COLLECTION)


def create_weaviate_collection_selection():
    weaviate_collections = get_weaviate_access().client.collections.list_all(simple=False)
    collections = [key for key in weaviate_collections.keys()]

    if not collections:
        st.info('No collections found in Weaviate')
        return

    if LKEY_SELECTED_WEAVIATE_COLLECTION in st.session_state:
        index = collections.index(st.session_state.get(LKEY_SELECTED_WEAVIATE_COLLECTION))
    elif KEY_SELECTED_WEAVIATE_COLLECTION in st.session_state:
        index = collections.index(st.session_state.get(KEY_SELECTED_WEAVIATE_COLLECTION))
    else:
        index = 0

    with (st.container(border=True)):
        st.selectbox('Select an existing Weaviate collection',
                     options=collections,
                     key=LKEY_SELECTED_WEAVIATE_COLLECTION,
                     index=index)

        if st.button("Load Weaviate collection"):
            change_weaviate_collection()
