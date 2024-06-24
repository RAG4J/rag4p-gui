import streamlit as st
from dotenv import load_dotenv
from rag4p.util.key_loader import KeyLoader

from rag4p_gui.my_menu import show_menu_prompting
from rag4p_gui.prompting_sidebar import PromptingSidebar
from rag4p_gui.session import init_session
from rag4p_gui.util.generation import construct_answer

load_dotenv()
key_loader = KeyLoader()


st.set_page_config(page_title='RAG4P GUI ~ Generating', page_icon='🧠', layout='wide')
init_session()
sidebar = PromptingSidebar()
sidebar()
show_menu_prompting()

st.write("## Prompting")

with st.form("prompt-form", border=True):
    context = st.text_area("Context", height=200)
    question = st.text_input("Question")
    submit_button = st.form_submit_button("Generate answer")

    if submit_button:
        answer = construct_answer(answer_context=context, question=question, key_loader=key_loader)

        st.write("Answer:")

        st.write(answer)