import streamlit as st
from dotenv import load_dotenv
from rag4p.integrations.ollama.access_ollama import AccessOllama
from rag4p.integrations.ollama.ollama_embedder import OllamaEmbedder
from rag4p.rag.embedding.local.onnx_embedder import OnnxEmbedder
from rag4p.util.key_loader import KeyLoader

from rag4p_gui.my_menu import show_menu, show_menu_indexing
from rag4p_gui.my_sidebar import MySidebar
from rag4p_gui.session import init_session
from rag4p.integrations.openai.openai_embedder import OpenAIEmbedder

from rag4p_gui.util.embedding import create_embedder

load_dotenv()


def embed_document():
    try:
        embedder = create_embedder(embedder_name=st.session_state.selected_embedder,
                                   model_name=st.session_state.selected_embedding_model)
    except ValueError:
        result_container.write('Unknown embedder')
        return

    text_to_embed = st.session_state.get('text_to_embed')
    embedding = embedder.embed(text=text_to_embed)
    st.session_state['input_embedding'] = embedding
    result_container.write(f'Length of Embedding: {len(embedding)}')


st.set_page_config(page_title='RAG4P GUI ~ Embeddings', page_icon='🧠', layout='wide')
init_session()

sidebar = MySidebar(embeddings=st.session_state.available_embedders)
sidebar.add_sidebar()
show_menu_indexing()

key_loader = KeyLoader()

st.write("## Embeddings")

chosen_embedder = st.session_state.selected_embedder
chosen_model = st.session_state.selected_embedding_model

st.text_input(label='Text to embed', key='text_to_embed')

result_container = st.container()

if st.session_state.get('text_to_embed') is not None and len(st.session_state.get('text_to_embed')) > 0:
    embed_document()

