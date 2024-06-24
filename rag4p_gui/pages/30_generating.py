import streamlit as st
from dotenv import load_dotenv
from rag4p.util.key_loader import KeyLoader

from rag4p_gui.components.select_number_of_chunks import KEY_AMOUNT_OF_CHUNKS
from rag4p_gui.components.select_strategy import strategy_available
from rag4p_gui.containers import show_retriever_information
from rag4p_gui.generating_sidebar import GeneratingSidebar
from rag4p_gui.my_menu import show_menu_prompting
from rag4p_gui.retrieval_sidebar import KEY_RETRIEVAL_STRATEGY
from rag4p_gui.session import init_session
from rag4p_gui.util.generation import construct_answer

load_dotenv()
key_loader = KeyLoader()


def retrieve_chunks_with_strategy(query: str):
    if KEY_RETRIEVAL_STRATEGY not in st.session_state:
        st.error("No retrieval strategy selected")
        return
    strategy = st.session_state[KEY_RETRIEVAL_STRATEGY]
    return strategy.retrieve_max_results(query, st.session_state[KEY_AMOUNT_OF_CHUNKS])


st.set_page_config(page_title='RAG4P GUI ~ Generating', page_icon='🧠', layout='wide')
init_session()
sidebar = GeneratingSidebar()
sidebar()
show_menu_prompting()

st.write("## Generating")

with st.expander("Show content store details"):
    show_retriever_information()

if strategy_available():
    input_container = st.container()
    result_container = st.container()

    with input_container:
        query = st.text_input(label='Query for')
        if st.button("Retrieve chunks"):
            response = retrieve_chunks_with_strategy(query)
            answer = construct_answer(answer_context=response.construct_context(),
                                      question=query,
                                      key_loader=key_loader)
            with result_container:
                st.info(f"""Generated answer:  
                {answer}""")

            with st.expander("Show provided context"):
                st.write(f"{response.construct_context()}")
