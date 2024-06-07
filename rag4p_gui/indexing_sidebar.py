import streamlit as st

from rag4p_gui.components.select_embedder import create_embedder_selector
from rag4p_gui.components.select_splitter import create_splitter_selector


def add_indexing_sidebar():
    with st.sidebar:
        st.title('Configure')
        embedder_container = st.container(border=True)
        splitter_container = st.container(border=True)

        create_embedder_selector(embedder_container)
        create_splitter_selector(splitter_container)
