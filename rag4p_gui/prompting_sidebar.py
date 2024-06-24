import streamlit as st

from rag4p_gui.components.select_llm import create_llm_selection
from rag4p_gui.retrieval_sidebar import RetrievalSidebar


class PromptingSidebar:

    def __init__(self):
        super().__init__()

    def __call__(self):
        with st.sidebar:
            st.title('Configure')
            llm_container = st.container(border=True)

            create_llm_selection(llm_container)
