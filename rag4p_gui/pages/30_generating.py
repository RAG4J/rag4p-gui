import streamlit as st

from rag4p_gui.my_menu import show_menu
from rag4p_gui.my_sidebar import MySidebar
from rag4p_gui.session import init_session

st.set_page_config(page_title='RAG4P GUI ~ Generating', page_icon='🧠', layout='wide')
init_session()

sidebar = MySidebar(embeddings=st.session_state.available_embedders)
sidebar.add_sidebar()
show_menu()

st.write("## Generating")
