import streamlit as st

from rag4p_gui.my_menu import show_menu
from rag4p_gui.my_sidebar import MySidebar
from rag4p_gui.session import init_session


st.set_page_config(page_title='RAG4P GUI', page_icon='🧠', layout='wide')

init_session()
sidebar = MySidebar(embeddings=st.session_state.available_embedders)
sidebar.add_sidebar()

show_menu()


st.title('RAG4P Experimental GUI')
st.markdown(
    f"""
    This is an experimental GUI for the RAG4P project. You can use this GUI to interact with the RAG4P API. 
    You can configure the embedding model to use in the sidebar.    
    """
)
if st.session_state.get('selected_embedder'):
    st.markdown(f"""
    Your choosen configuration is:
    - Embedder: '_{st.session_state.selected_embedder}_'.
    - Embedding model: '_{st.session_state.selected_embedding_model}_'.
    """)

