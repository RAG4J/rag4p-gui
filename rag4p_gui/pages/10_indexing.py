import asyncio
import os
import streamlit_antd_components as sac
import streamlit as st
from dotenv import load_dotenv
from rag4p.rag.store.local.internal_content_store import InternalContentStore

from rag4p_gui.containers import info_content_store
from rag4p_gui.data.data_sets import load_internal_content_store, available_content_stores, available_data_files, \
    content_store_metadata_from_backup
from rag4p_gui.data.readers.wordpress_jsonl_reader import WordpressJsonlReader
from rag4p_gui.my_menu import show_menu_indexing
from rag4p_gui.my_sidebar import MySidebar
from rag4p_gui.session import init_session
from rag4p_gui.util.embedding import create_embedder

load_dotenv()


async def initialize_content_store():
    dataset = st.session_state.selected_data_file
    # TODO What if we have another reader?
    # wordpress_path = os.path.join(dataset['path'], dataset['file'])
    _content_store = await load_internal_content_store(
        content_reader=WordpressJsonlReader(file_name=f"{dataset['path']}/{dataset['file']}"),
        splitter_name=st.session_state.selected_splitter,
        embedder_name=st.session_state.selected_embedder,
        embedding_model=st.session_state.selected_embedding_model,
        chunk_size=st.session_state.chunk_size
    )
    st.session_state.content_store = _content_store
    st.session_state.content_store_initialized = True
    st.session_state.content_store_embedding_model = st.session_state.selected_embedding_model


def load_content_store():
    asyncio.run(initialize_content_store())


def load_content_store_from_backup():
    backup_path = f"../../data_backups/{st.session_state.selected_content_store}"

    current_script_path = os.path.dirname(os.path.realpath(__file__))
    combined_path = os.path.join(current_script_path, backup_path)
    normalized_path = os.path.normpath(combined_path)

    metadata = content_store_metadata_from_backup(backup_path)
    _content_store = InternalContentStore.load_from_backup(
        embedder=create_embedder(embedder_name=metadata['supplier'], model_name=metadata['model']),
        path=normalized_path)
    st.session_state.content_store = _content_store
    st.session_state.content_store_initialized = True


# def info_content_store(st_container):
#     if 'content_store' in st.session_state and st.session_state.content_store is not None:
#         num_chunks = 0
#         for chunk in st.session_state.content_store.loop_over_chunks():
#             num_chunks += 1
#         metadata = st.session_state.content_store.get_metadata()
#         st_container.markdown(
#             f"""
#             *Number of chunks*: **{num_chunks}**
#
#             *Embedder*: **{metadata["supplier"]}**
#
#             *Embedding model*: **{metadata["model"]}**
#         """)
#     else:
#         st_container.info('No content found, while it should be there.')


st.set_page_config(page_title='RAG4P GUI ~ Indexing', page_icon='🧠', layout='wide')
init_session()

sidebar = MySidebar(embeddings=st.session_state.available_embedders)
sidebar.add_sidebar()
show_menu_indexing()

st.write("## Indexing")

st.markdown(f"""
There is no RAG system without content. In this section, you can index documents to be used in the RAG system. 
You have to make a choice for the retrieval system to use. We support an internal content store, and Weaviate.

With the choice of a retrieval system, you must choose the dataset to use. You can load a new one using your selected
embedder and embedding model. You can also load a backup of a content store. 
""")

datasets = available_data_files()
stores = available_content_stores()

column1, column2 = st.columns(2)
with column1:
    st.selectbox('Select a dataset', options=datasets['available'], key='selected_data_file',
                 format_func=lambda x: x['name'])

    if st.button("Initialize Content Store"):
        asyncio.run(initialize_content_store())

with column2:
    st.selectbox('Select a Content Store backup', stores, key='selected_content_store')
    if st.button("Load Content Store backup"):
        load_content_store_from_backup()

sac.divider(label="Show information about the loaded content store:")
result_container = st.container()
if st.session_state.get("content_store_initialized"):
    info_content_store(result_container)
else:
    result_container.write("Content store not initialized or still initializing")
