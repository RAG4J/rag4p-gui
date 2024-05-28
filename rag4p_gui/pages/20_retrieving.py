import streamlit as st
from rag4p.rag.retrieval.strategies.window_retrieval_strategy import WindowRetrievalStrategy

from rag4p_gui.containers import info_content_store
from rag4p_gui.my_menu import show_menu
from rag4p_gui.my_sidebar import MySidebar
from rag4p_gui.session import init_session


def retrieve_chunks():
    text_to_find = st.session_state.text_to_find
    found_chunks = content_store.find_relevant_chunks(text_to_find)
    result_container.write(f'Found {len(found_chunks)} chunks')
    for chunk in found_chunks:
        result_container.write(f"{chunk.score:.3f} - {chunk.chunk_text}")


def retrieve_chunks_with_strategy():
    text_to_find = st.session_state.text_to_find
    retrieval_output = strategy.retrieve_max_results(text_to_find, 2)
    result_container.write(f"Found {len(retrieval_output.items)} relevant chunks")
    for item in retrieval_output.items:
        result_container.write(f"Document: {item.document_id}, Chunk id: {item.chunk_id}, Text: {item.text}")

    result_container.write(f"Text: {retrieval_output.construct_context()}")


def check_content_store_embedding_model():
    if "content_store" not in st.session_state or st.session_state.content_store is None:
        st.error("Please index some documents first and initialise the content store.")
        st.stop()

    if 'content_store_embedding_model' in st.session_state:
        if st.session_state.content_store_embedding_model != st.session_state.selected_embedding_model:
            st.warning(f"Content store was initialized with a different embedding model: "
                       f"{st.session_state.content_store_embedding_model}. "
                       f"Please re-index the documents with the new embedding model.")


st.set_page_config(page_title='RAG4P GUI ~ Retrieving', page_icon='🧠', layout='wide')
init_session()

sidebar = MySidebar(embeddings=st.session_state.available_embedders)
sidebar.add_sidebar()
show_menu()

st.write("## Retrieving")
st.markdown("When using the internal content store, you can use the session state to obtain the store.")


check_content_store_embedding_model()

content_store = st.session_state.content_store
strategy = WindowRetrievalStrategy(retriever=content_store, window_size=1)

info_content_store(st.container())

st.text_input(label='Query for', key='text_to_find')

result_container = st.container()

if st.session_state.get('text_to_find') is not None and len(st.session_state.get('text_to_find')) > 0:
    retrieve_chunks_with_strategy()

