import streamlit as st

from rag4p.util.key_loader import KeyLoader
from rag4p.integrations.opensearch.opensearch_client import OpenSearchClient
from rag4p_gui.integrations.opensearch import ENABLE_OPENSEARCH_KEY
from rag4p.integrations.opensearch.connection_builder import build_aws_search_service


@st.cache_resource
def get_opensearch_access():
    key_loader = KeyLoader()

    try:
        opensearch_conn = build_aws_search_service(stack_name=key_loader.get_property("OPENSEARCH_STACK_NAME"),
                                                   application_prefix=key_loader.get_property("OPENSEARCH_APP_PREFIX"))
        opensearch_client = OpenSearchClient(opensearch_conn)
        return opensearch_client
    except Exception as e:
        raise NoAwsSessionError(f"Could not connect to OpenSearch '{e}'")


def enable_opensearch(key_loader: KeyLoader = KeyLoader()):
    return key_loader.get_property(ENABLE_OPENSEARCH_KEY) == 'True'

class NoAwsSessionError(Exception):
    pass
