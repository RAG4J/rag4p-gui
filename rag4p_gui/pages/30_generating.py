import streamlit as st
from dotenv import load_dotenv
from rag4p.integrations.ollama.access_ollama import AccessOllama
from rag4p.integrations.ollama.ollama_answer_generator import OllamaAnswerGenerator
from rag4p.integrations.openai.openai_answer_generator import OpenaiAnswerGenerator
from rag4p.integrations.bedrock.bedrock_answer_generator import BedrockAnswerGenerator
from rag4p.integrations.bedrock.access_bedrock import AccessBedrock
from rag4p.util.key_loader import KeyLoader

from rag4p_gui.components.select_content_store import KEY_SELECTED_CONTENT_STORE
from rag4p_gui.components.select_llm import KEY_SELECTED_LLM_PROVIDER, KEY_SELECTED_LLM_MODEL
from rag4p_gui.components.select_number_of_chunks import KEY_AMOUNT_OF_CHUNKS
from rag4p_gui.components.select_opensearch_collection import KEY_SELECTED_OPENSEARCH_COLLECTION
from rag4p_gui.components.select_strategy import KEY_SELECTED_STRATEGY, strategy_available
from rag4p_gui.components.select_weaviate_collection import KEY_SELECTED_WEAVIATE_COLLECTION
from rag4p_gui.generating_sidebar import GeneratingSidebar
from rag4p_gui.my_menu import show_menu
from rag4p_gui.retrieval_sidebar import KEY_RETRIEVAL_STRATEGY
from rag4p_gui.session import init_session

load_dotenv()
key_loader = KeyLoader()


def retrieve_chunks_with_strategy(query: str):
    if KEY_RETRIEVAL_STRATEGY not in st.session_state:
        st.error("No retrieval strategy selected")
        return
    strategy = st.session_state[KEY_RETRIEVAL_STRATEGY]
    return strategy.retrieve_max_results(query, st.session_state[KEY_AMOUNT_OF_CHUNKS])


def construct_answer(answer_context: str, question: str):
    if KEY_SELECTED_LLM_PROVIDER not in st.session_state or KEY_SELECTED_LLM_MODEL not in st.session_state:
        st.error("No LLM provider or model selected")
        return

    model_ = st.session_state[KEY_SELECTED_LLM_MODEL]
    if st.session_state[KEY_SELECTED_LLM_PROVIDER].lower() == 'ollama':
        access_ollama = AccessOllama()
        answer_generator = OllamaAnswerGenerator(access_ollama=access_ollama, model=model_)
    elif st.session_state[KEY_SELECTED_LLM_PROVIDER].lower() == 'openai':
        answer_generator = OpenaiAnswerGenerator(openai_api_key=key_loader.get_openai_api_key(), openai_model=model_)
    elif st.session_state[KEY_SELECTED_LLM_PROVIDER].lower() == 'bedrock':
        access_bedrock = AccessBedrock()
        answer_generator = BedrockAnswerGenerator(model=model_, access_bedrock=access_bedrock)
    else:
        st.error("No LLM provider selected")
        return

    return answer_generator.generate_answer(question=question, context=answer_context)


st.set_page_config(page_title='RAG4P GUI ~ Generating', page_icon='🧠', layout='wide')
init_session()
sidebar = GeneratingSidebar()
sidebar()
show_menu()

st.write("## Generating")

if KEY_SELECTED_WEAVIATE_COLLECTION in st.session_state:
    st.write(f"Selected Weaviate collection: {st.session_state[KEY_SELECTED_WEAVIATE_COLLECTION]}")
if KEY_SELECTED_CONTENT_STORE in st.session_state:
    st.write(f"Selected content store: {st.session_state[KEY_SELECTED_CONTENT_STORE]}")
if KEY_SELECTED_OPENSEARCH_COLLECTION in st.session_state:
    st.write(f"Selected OpenSearch index: {st.session_state[KEY_SELECTED_OPENSEARCH_COLLECTION]}")
if KEY_SELECTED_STRATEGY in st.session_state:
    st.write(f"Selected strategy: {st.session_state[KEY_SELECTED_STRATEGY]}")
if KEY_SELECTED_LLM_PROVIDER in st.session_state:
    st.write(f"Selected LLM provider: {st.session_state[KEY_SELECTED_LLM_PROVIDER]}")
if KEY_SELECTED_LLM_MODEL in st.session_state:
    st.write(f"Selected LLM model: {st.session_state[KEY_SELECTED_LLM_MODEL]}")

if strategy_available():
    input_container = st.container()
    result_container = st.container()

    with input_container:
        query = st.text_input(label='Query for')
        if st.button("Retrieve chunks"):
            response = retrieve_chunks_with_strategy(query)
            answer = construct_answer(response.construct_context(), query)
            with result_container:
                st.info(f"""Generated answer:  
                {answer}""")
                st.write(f"{response.construct_context()}")
