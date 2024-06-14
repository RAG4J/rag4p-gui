import asyncio
import os

import streamlit as st
import streamlit_antd_components as sac
from dotenv import load_dotenv
from rag4p.indexing.indexing_service import IndexingService
from rag4p.indexing.splitters.max_token_splitter import MaxTokenSplitter
from rag4p.integrations.openai.openai_embedder import OpenAIEmbedder
from rag4p.integrations.opensearch.opensearch_content_store import OpenSearchContentStore
from rag4p.integrations.weaviate.chunk_collection import weaviate_properties
from rag4p.integrations.weaviate.weaviate_content_store import WeaviateContentStore
from rag4p.util.key_loader import KeyLoader

from rag4p_gui.components.select_content_store import create_content_store_selection
from rag4p_gui.components.select_weaviate_collection import create_weaviate_collection_selection
from rag4p_gui.containers import info_content_store
from rag4p_gui.data.data_sets import load_internal_content_store, available_data_files
from rag4p_gui.data.readers.teqnation_jsonl_reader import TeqnationJsonlReader
from rag4p_gui.data.readers.wordpress_jsonl_reader import WordpressJsonlReader
from rag4p_gui.indexing_sidebar import add_indexing_sidebar
from rag4p_gui.integrations.opensearch.connect import get_opensearch_access
from rag4p_gui.integrations.opensearch.indexing import update_template
from rag4p_gui.integrations.weaviate import luminis, teqnation
from rag4p_gui.integrations.weaviate.connect import get_weaviate_access
from rag4p_gui.my_menu import show_menu_indexing
from rag4p_gui.session import init_session, KEY_SELECTED_EMBEDDER
from rag4p_gui.util.embedding import create_embedder
from rag4p_gui.util.splitter import create_splitter

load_dotenv()
key_loader = KeyLoader()


async def initialize_content_store():
    dataset = st.session_state.selected_data_file

    kwargs = {
        'provider': st.session_state.selected_embedder.lower(),
    }
    kwargs.update(**dataset)
    if st.session_state.selected_splitter == MaxTokenSplitter.name():
        kwargs['chunk_size'] = st.session_state.chunk_size

    reader, additional_properties = _create_reader(dataset)

    _content_store = await load_internal_content_store(
        content_reader=reader,
        splitter_name=st.session_state.selected_splitter,
        embedder_name=st.session_state.selected_embedder,
        embedding_model=st.session_state.selected_embedding_model,
        **kwargs
    )
    st.session_state.content_store = _content_store
    st.session_state.content_store_initialized = True
    st.session_state.content_store_embedding_model = st.session_state.selected_embedding_model


async def initialize_weaviate_content_store():
    if st.session_state.selected_embedder != OpenAIEmbedder.supplier():
        raise ValueError(f"Embedder {st.session_state.selected_embedder} not supported for Weaviate")

    dataset = st.session_state.selected_data_file

    kwargs = {
        'provider': st.session_state.selected_embedder.lower(),
    }
    kwargs.update(**dataset)
    if st.session_state.selected_splitter == MaxTokenSplitter.name():
        kwargs['chunk_size'] = st.session_state.chunk_size

    reader, additional_properties = _create_reader(dataset)

    kwargs['embedding_model'] = st.session_state.selected_embedding_model

    _collection_name = st.session_state.new_collection_name
    _embedder = create_embedder(embedder_name=st.session_state.selected_embedder,
                                model_name=st.session_state.selected_embedding_model)
    _splitter = create_splitter(splitter_name=st.session_state.selected_splitter, **kwargs)
    _content_store = WeaviateContentStore(weaviate_access=get_weaviate_access(),
                                          embedder=_embedder,
                                          collection_name=_collection_name)
    get_weaviate_access().force_create_collection(collection_name=_collection_name,
                                                  properties=weaviate_properties(additional_properties))
    indexing_service = IndexingService(content_store=_content_store)
    response = indexing_service.index_documents(content_reader=reader, splitter=_splitter)
    print(response)


async def initialize_opensearch_content_store():
    if st.session_state.selected_embedder != OpenAIEmbedder.supplier():
        raise ValueError(f"Embedder {st.session_state.selected_embedder} not supported for OpenSearch")

    dataset = st.session_state.selected_data_file

    kwargs = {
        'provider': st.session_state.selected_embedder.lower(),
    }
    kwargs.update(**dataset)
    if st.session_state.selected_splitter == MaxTokenSplitter.name():
        kwargs['chunk_size'] = st.session_state.chunk_size

    reader, additional_properties = _create_reader(dataset)

    kwargs['embedding_model'] = st.session_state.selected_embedding_model

    _collection_name = st.session_state.new_collection_name
    _embedder = create_embedder(embedder_name=st.session_state.selected_embedder,
                                model_name=st.session_state.selected_embedding_model)
    _splitter = create_splitter(splitter_name=st.session_state.selected_splitter, **kwargs)

    opensearch_client = get_opensearch_access()
    embedder_size = len(_embedder.embed("test"))
    update_template(opensearch_client=opensearch_client,
                    index_name=_collection_name,
                    dataset=dataset,
                    embedding_dimension=embedder_size)

    index_name = opensearch_client.create_index(provided_alias_name=_collection_name)

    _content_store = OpenSearchContentStore(opensearch_client=opensearch_client,
                                            embedder=_embedder,
                                            index_name=index_name)
    indexing_service = IndexingService(content_store=_content_store)
    response = indexing_service.index_documents(content_reader=reader, splitter=_splitter)
    print(response)
    opensearch_client.switch_alias_to(index_name=index_name, provided_alias_name=_collection_name)


def _create_reader(dataset):
    data_path = str(os.path.join(dataset['path'], dataset['file']))
    if dataset['reader'] == WordpressJsonlReader.__name__:
        reader = WordpressJsonlReader(file_name=data_path)
        additional_properties = luminis.additional_properties
    elif dataset['reader'] == TeqnationJsonlReader.__name__:
        reader = TeqnationJsonlReader(file_name=data_path)
        additional_properties = teqnation.additional_properties
    else:
        raise ValueError(f"Unknown reader {dataset['reader']}")
    return reader, additional_properties


st.set_page_config(page_title='RAG4P GUI ~ Indexing', page_icon='🧠', layout='wide')
init_session()

add_indexing_sidebar()
show_menu_indexing()

st.write("## Indexing")

st.markdown(f"""
There is no RAG system without content. In this section, you can index documents to be used in the RAG system. 
You have to make a choice for the retrieval system to use. We support an internal content store, and Weaviate.

With the choice of a retrieval system, you must choose the dataset to use. You can load a new one using your selected
embedder and embedding model. You can also load a backup of a content store. 
""")

datasets = available_data_files()

column1, column2 = st.columns(2)
with column1:
    st.selectbox('Select a dataset', options=datasets['available'], key='selected_data_file',
                 format_func=lambda x: x['name'])

    if st.button("Initialize Content Store"):
        asyncio.run(initialize_content_store())

with column2:
    st.text_input("Enter a new collection name", key="new_collection_name")
    if st.button("Initialize Weaviate Content Store"):
        asyncio.run(initialize_weaviate_content_store())
    if st.button("Initialize OpenSearch Content Store"):
        asyncio.run(initialize_opensearch_content_store())

result_container = st.container()
if st.session_state.get("content_store_initialized"):
    info_content_store(result_container)
else:
    result_container.write("Content store not initialized or still initializing")

sac.divider(label="Create a backup of the content store")
if st.session_state.get("content_store_initialized"):
    meta = st.session_state.content_store.get_metadata()
    if 'backup_file' not in meta:
        st.write(
            f"Create a backup of the current content store loaded from {st.session_state.selected_data_file['name']}")
        file_name = (st.session_state.selected_data_file['name'].replace(" ", "_").lower() + "_"
                     + st.session_state[KEY_SELECTED_EMBEDDER].lower())
        st.text_input("Enter Backup name", key="backup_name", value=f"{file_name}")
        if st.button("Create backup"):
            st.session_state.content_store.add_metadata('name', st.session_state.backup_name)
            st.session_state.content_store.add_metadata('backup_file', f"data_backups/{st.session_state.backup_name}")
            st.session_state.content_store.backup(f"data_backups/{st.session_state.backup_name}")

sac.divider(label="Show available content stores")

column1, column2 = st.columns(2)
with column1:
    create_content_store_selection()
with column2:
    create_weaviate_collection_selection()
