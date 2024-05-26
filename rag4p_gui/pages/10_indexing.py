import asyncio
from asyncio import Lock

import streamlit as st
from dotenv import load_dotenv
from rag4p.indexing.indexing_service import IndexingService
from rag4p.rag.store.local.internal_content_store import InternalContentStore

from rag4p_gui.data.readers.wordpress_jsonl_reader import WordpressJsonlReader
from rag4p_gui.my_menu import show_menu_indexing
from rag4p_gui.my_sidebar import MySidebar
from rag4p_gui.session import init_session
from rag4p_gui.util.embedding import create_embedder
from rag4p_gui.util.splitter import create_splitter

load_dotenv()

content_store = None
content_store_lock = Lock()


async def load_internal_content_store(splitter_name: str, embedder_name: str, embedding_model: str, chunk_size: int):
    try:
        embedder = create_embedder(embedder_name=embedder_name, model_name=embedding_model)
    except ValueError:
        return None, f"The name of the provided embedder '{embedder_name}' is unknown. Please select a valid embedder."

    internal_content_store = InternalContentStore(embedder=embedder)
    message, splitter = create_splitter(splitter_name=splitter_name,
                                        embedding_model=embedding_model,
                                        chunk_size=chunk_size)
    indexing_service = IndexingService(content_store=internal_content_store)
    content_reader = WordpressJsonlReader("short_wordpress.jsonl")
    indexing_service.index_documents(content_reader=content_reader, splitter=splitter)

    return internal_content_store, message


async def initialize_content_store():
    result_container.info('Loading content store...')

    async with content_store_lock:
        if 'content_store' not in st.session_state:
            result_container.info('About to load the content store...')
            _content_store, message = await load_internal_content_store(
                splitter_name=st.session_state.selected_splitter,
                embedder_name=st.session_state.selected_embedder,
                embedding_model=st.session_state.selected_embedding_model,
                chunk_size=st.session_state.chunk_size
            )
            result_container.info(message)
    return content_store


async def load_content_store():
    st.session_state.content_store = await initialize_content_store()
    st.session_state.content_store_initialized = True


def info_content_store():
    if 'content_store' in st.session_state:
        num_chunks = 0
        for chunk in st.session_state.content_store.loop_over_chunks():
            num_chunks += 1
        result_container.write(f'Number of chunks: {num_chunks}')
    else:
        result_container.info('No content found, while it should be there.')


if 'content_store_initialized' not in st.session_state:
    st.session_state.content_store_initialized = False


st.set_page_config(page_title='RAG4P GUI ~ Indexing', page_icon='🧠', layout='wide')
init_session()

sidebar = MySidebar(embeddings=st.session_state.available_embedders)
sidebar.add_sidebar()
show_menu_indexing()

st.write("## Indexing")

st.markdown(f"""
There is no RAG system without content. In this section, you can index documents to be used in the RAG system. 
You have to make a choice for the retrieval system to use. We support an internal content store, and Weaviate.

With the choice of a retrieval system, you must choose the dataset to use.  
""")

result_container = st.container()
if st.button("Initialize Content Store"):
    if not st.session_state.content_store_initialized:
        asyncio.run(load_content_store())
    else:
        st.warning("Content store is already initialized!")

if st.session_state.get("content_store_initialized"):
    info_content_store()
else:
    result_container.write("Content store not initialized or still initializing")
