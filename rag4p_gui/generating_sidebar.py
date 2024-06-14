import streamlit as st

from rag4p_gui.components.select_content_store import create_content_store_selection
from rag4p_gui.components.select_llm import create_llm_selection
from rag4p_gui.components.select_number_of_chunks import create_number_of_chunks_selection
from rag4p_gui.components.select_opensearch_collection import create_opensearch_collection_selection
from rag4p_gui.components.select_retriever import create_retriever_selection, KEY_CHOSEN_RETRIEVER
from rag4p_gui.components.select_strategy import create_retrieval_strategy_selection
from rag4p_gui.components.select_weaviate_collection import create_weaviate_collection_selection
from rag4p_gui.retrieval_sidebar import RetrievalSidebar


class GeneratingSidebar(RetrievalSidebar):

    def __init__(self):
        super().__init__()

    def __call__(self):
        with st.sidebar:
            st.title('Configure')
            llm_container = st.container(border=True)
            chunks_container = st.container(border=True)
            strategy_container = st.container(border=True)
            choose_retriever_container = st.container(border=True)

            create_llm_selection(llm_container)
            create_content_store_selection()
            create_weaviate_collection_selection()
            create_opensearch_collection_selection()

            create_retriever_selection(choose_retriever_container)

            create_number_of_chunks_selection(chunks_container)
            create_retrieval_strategy_selection(strategy_container)
