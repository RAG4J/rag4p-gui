import streamlit as st
import streamlit_antd_components as sac

from rag4p_gui.components.select_opensearch_collection import KEY_SELECTED_OPENSEARCH_COLLECTION
from rag4p_gui.components.select_retriever import VALUE_CHOSEN_RETRIEVER_WEAVIATE, KEY_CHOSEN_RETRIEVER, \
    VALUE_CHOSEN_RETRIEVER_INTERNAL, VALUE_CHOSEN_RETRIEVER_OPENSEARCH
from rag4p_gui.components.select_weaviate_collection import KEY_SELECTED_WEAVIATE_COLLECTION
from rag4p_gui.data.content_store_metadata import ContentStoreMetadata
from rag4p_gui.integrations.opensearch.connect import get_opensearch_access
from rag4p_gui.integrations.opensearch.indexing import OpenSearchContentStoreMetadataService
from rag4p_gui.integrations.weaviate.connect import get_weaviate_access
from rag4p_gui.integrations.weaviate.indexing import WeaviateContentStoreMetadataService


def info_content_store(st_container):
    with st_container:

        sac.divider(label="Loaded content store:", align='center')
    if 'content_store' in st.session_state and st.session_state.content_store is not None:
        num_chunks = 0
        for chunk in st.session_state.content_store.loop_over_chunks():
            num_chunks += 1
        metadata = st.session_state.content_store.get_metadata()
        col1, col2 = st_container.columns(2)
        with col1:
            st.markdown(
                f"""
                *Name*: **{metadata["name"]}**
                
                *Number of chunks*: **{num_chunks}**
                
                *Create date*: **{metadata["create_date"] if "create_date" in metadata.keys() else "unknown"}**

                *Embedder*: **{metadata["supplier"]}**
    
                *Embedding model*: **{metadata["model"]}**
                
                *Splitter*: **{metadata["splitter"] if "splitter" in metadata.keys() else "unknown"}**
                """
            )
        with col2:
            for key in metadata.keys():
                if key not in ['create_date', 'supplier', 'model', 'splitter', 'embedder', 'embedding_model', 'name']:
                    st.markdown(f"*{key}*: **{metadata[key]}**")

    else:
        st_container.info('No content found, while it should be there.')


def info_metadata_content_store(st_container, metadata: ContentStoreMetadata):
    with st_container:
        sac.divider(label="Loaded content store:", align='center')
    if metadata is not None:
        col1, col2 = st_container.columns(2)
        with col1:
            st.markdown(
                f"""
                *Name*: **{metadata.collection_name}**
                
                *Create date*: **{metadata.created_at if metadata.created_at is not None else "unknown"}**

                *Embedder*: **{metadata.embedder}**
    
                *Embedding model*: **{metadata.embedding_model}**
                
                *Splitter*: **{metadata.splitter if metadata.splitter is not None else "unknown"}**

                *Chunk size*: **{metadata.chunk_size if metadata.chunk_size is not None else "unknown"}**
                                
                """
            )
        with col2:
            st.markdown(
                f"""
                *Dataset*: **{metadata.dataset}**
                
                *Number of documents*: **{metadata.num_documents}**
                
                *Number of chunks*: **{metadata.num_chunks}**
                
                *Running time*: **{metadata.running_time}**
                
                *Content reader*: **{metadata.contentReader}**
                """
            )

    else:
        st_container.info('No content found, while it should be there.')


def show_retriever_information():
    if KEY_CHOSEN_RETRIEVER not in st.session_state:
        st.write(f"You need to select a retriever first.")
    else:
        container = st.container()
        if st.session_state[KEY_CHOSEN_RETRIEVER] == VALUE_CHOSEN_RETRIEVER_INTERNAL:
            info_content_store(container)
        elif st.session_state[KEY_CHOSEN_RETRIEVER] == VALUE_CHOSEN_RETRIEVER_WEAVIATE:
            collection_ = st.session_state[KEY_SELECTED_WEAVIATE_COLLECTION]
            metadata = WeaviateContentStoreMetadataService(get_weaviate_access()).get_meta_data(collection_)
            info_metadata_content_store(container, metadata)

            schema = get_weaviate_access().obtain_meta_for_collection(collection_)

            with container:
                properties = [f"{prop.name} ({prop.data_type.split('.')[-1]})" for prop in schema["collection"].properties]
                properties_str = ', '.join(properties)
                st.markdown(f"""Fields:  
                {properties_str}""")
        elif st.session_state[KEY_CHOSEN_RETRIEVER] == VALUE_CHOSEN_RETRIEVER_OPENSEARCH:
            collection_ = st.session_state[KEY_SELECTED_OPENSEARCH_COLLECTION]
            metadata = OpenSearchContentStoreMetadataService(get_opensearch_access()).get_meta_data(collection_)
            info_metadata_content_store(container, metadata)

            details = get_opensearch_access().client().indices.get(index=collection_)
            index_name = list(details.keys())[0]
            props = details[index_name]['mappings']['properties']
            property_names = [prop for prop in props]
            properties = [f"{name} ({props[name]['type']})" for name in property_names]
            properties_str = ', '.join(properties)
            with container:
                st.write(f"Index: {index_name}")
                st.write(properties_str)
        else:
            st.error("Unknown retriever")
