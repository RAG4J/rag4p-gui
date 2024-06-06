import streamlit as st
import streamlit_antd_components as sac

from dotenv import load_dotenv

from rag4p_gui.components.select_content_store import KEY_SELECTED_CONTENT_STORE
from rag4p_gui.components.select_number_of_chunks import KEY_AMOUNT_OF_CHUNKS
from rag4p_gui.components.select_strategy import KEY_SELECTED_STRATEGY, strategy_available
from rag4p_gui.components.select_weaviate_collection import KEY_SELECTED_WEAVIATE_COLLECTION
from rag4p_gui.containers import info_content_store
from rag4p_gui.integrations.weaviate.connect import get_weaviate_access
from rag4p_gui.my_menu import show_menu
from rag4p_gui.retrieval_sidebar import RetrievalSidebar, KEY_RETRIEVAL_STRATEGY, KEY_CHOSEN_RETRIEVER, \
    VALUE_CHOSEN_RETRIEVER_INTERNAL, VALUE_CHOSEN_RETRIEVER_WEAVIATE
from rag4p_gui.session import init_session

load_dotenv()


def retrieve_chunks_with_strategy():
    strategy = st.session_state[KEY_RETRIEVAL_STRATEGY]
    text_to_find = st.session_state.text_to_find
    retrieval_output = strategy.retrieve_max_results(text_to_find, st.session_state[KEY_AMOUNT_OF_CHUNKS])

    with result_container:
        st.write(f"Found {len(retrieval_output.items)} relevant chunks")
        for item in retrieval_output.items:
            st.markdown(f"Document: {item.document_id}, Chunk id: {item.chunk_id}")
            st.markdown(f"Chunk Text: {item.text}")

        sac.divider(label="Context")
        st.write(retrieval_output.construct_context())


st.set_page_config(page_title='RAG4P GUI ~ Retrieving', page_icon='🧠', layout='wide')
init_session()

sidebar = RetrievalSidebar()
sidebar()

show_menu()

st.write("## Retrieving")
st.markdown("When using the internal content store, you can use the session state to obtain the store.")

if KEY_SELECTED_WEAVIATE_COLLECTION in st.session_state:
    st.write(f"Selected collection: {st.session_state[KEY_SELECTED_WEAVIATE_COLLECTION]}")
if KEY_SELECTED_CONTENT_STORE in st.session_state:
    st.write(f"Selected content store: {st.session_state[KEY_SELECTED_CONTENT_STORE]}")
if KEY_SELECTED_STRATEGY in st.session_state:
    st.write(f"Selected strategy: {st.session_state[KEY_SELECTED_STRATEGY]}")

with st.expander("Show content store details"):
    if KEY_CHOSEN_RETRIEVER not in st.session_state:
        st.write(f"YOu need to select a retriever first.")
    else:
        if st.session_state[KEY_CHOSEN_RETRIEVER] == VALUE_CHOSEN_RETRIEVER_INTERNAL:
            info_content_store(st.container())
        elif st.session_state[KEY_CHOSEN_RETRIEVER] == VALUE_CHOSEN_RETRIEVER_WEAVIATE:
            # TODO replace with info from access object
            meta = get_weaviate_access().client.get_meta()
            collection_ = st.session_state[KEY_SELECTED_WEAVIATE_COLLECTION]
            if get_weaviate_access().does_collection_exist(collection_):
                meta["collection"] = get_weaviate_access().client.collections.export_config(name=collection_)
            st.write(meta)
        else:
            st.error("Unknown retriever")

if strategy_available():
    st.text_input(label='Query for', key='text_to_find')

    result_container = st.container()

    if st.session_state.get('text_to_find') is not None and len(st.session_state.get('text_to_find')) > 0:
        retrieve_chunks_with_strategy()
