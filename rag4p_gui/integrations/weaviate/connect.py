import streamlit as st


from rag4p.integrations.weaviate.access_weaviate import AccessWeaviate
from rag4p.util.key_loader import KeyLoader


@st.cache_resource
def get_weaviate_access():
    key_loader = KeyLoader()
    access_weaviate = AccessWeaviate(url=key_loader.get_weaviate_url(), access_key=key_loader.get_weaviate_api_key())

    return access_weaviate
