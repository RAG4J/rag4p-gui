import streamlit as st


from rag4p.integrations.weaviate.access_weaviate import AccessWeaviate
from rag4p_gui.integrations.weaviate import ENABLE_WEAVIATE_KEY
from rag4p.util.key_loader import KeyLoader


@st.cache_resource()
def get_weaviate_access():
    key_loader = KeyLoader()
    access_weaviate = AccessWeaviate(url=key_loader.get_weaviate_url(),
                                     access_key=key_loader.get_weaviate_api_key(),
                                     openai_api_key=key_loader.get_openai_api_key())

    return access_weaviate


def enable_weaviate(key_loader: KeyLoader = KeyLoader()):
    return key_loader.get_property(ENABLE_WEAVIATE_KEY) == 'True'