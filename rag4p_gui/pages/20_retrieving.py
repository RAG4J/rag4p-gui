import streamlit as st
import streamlit_antd_components as sac
from dotenv import load_dotenv

from rag4p_gui.components.select_number_of_chunks import KEY_AMOUNT_OF_CHUNKS
from rag4p_gui.components.select_strategy import strategy_available
from rag4p_gui.containers import show_retriever_information
from rag4p_gui.my_menu import show_menu
from rag4p_gui.retrieval_sidebar import RetrievalSidebar, KEY_RETRIEVAL_STRATEGY
from rag4p_gui.session import init_session

load_dotenv()


def retrieve_chunks_with_strategy(query):
    if KEY_RETRIEVAL_STRATEGY not in st.session_state:
        st.error("No retrieval strategy selected")
        return
    strategy = st.session_state[KEY_RETRIEVAL_STRATEGY]
    retrieval_output = strategy.retrieve_max_results(query, st.session_state[KEY_AMOUNT_OF_CHUNKS])

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

with st.expander("Show content store details"):
    show_retriever_information()

if strategy_available():
    input_container = st.container()
    result_container = st.container()

    with input_container:
        query = st.text_input(label='Query for')
        if st.button("Retrieve chunks"):
            retrieve_chunks_with_strategy(query)
