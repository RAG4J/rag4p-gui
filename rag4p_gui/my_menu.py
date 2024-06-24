import streamlit as st
import streamlit_antd_components as sac


def show_menu():
    page1, page2, page3, page4 = st.columns(4, gap="small")
    with page1:
        st.page_link(page="home.py", label="Home", icon="🏠", help="Go back to the home page")
    with page2:
        st.page_link(page="pages/10_indexing.py", label="Indexing", help="Indexing content into a store")
    with page3:
        st.page_link(page="pages/20_retrieving.py", label="Retrieving", help="Retrieving content")
    with page4:
        st.page_link(page="pages/30_generating.py", label="Generating", help="Generating content")

    sac.divider(label="Home")


def show_menu_indexing():
    page1, page2, page3, page4, page5 = st.columns(5, gap="small")
    with page1:
        st.page_link(page="home.py", label="Home", icon="🏠", help="Go back to the home page")
    with page2:
        st.page_link(page="pages/10_indexing.py", label="Indexing", help="Go back to the retrieving home")
    with page3:
        st.page_link(page="pages/11_embeddings.py", label="Embeddings", help="Learning embeddings")
    with page4:
        st.page_link(page="pages/12_chunking.py", label="Chunking", help="Learn about chunking")
    with page5:
        st.page_link(page="pages/13_tokenizing.py", label="Tokenizing", help="Learn about tokenization")

    sac.divider(label="Indexing")


def show_menu_prompting():
    page1, page2, page3 = st.columns(3, gap="small")
    with page1:
        st.page_link(page="home.py", label="Home", icon="🏠", help="Go back to the home page")

    with page2:
        st.page_link(page="pages/30_generating.py", label="Generating", help="Go back to Generating content")

    with page3:
        st.page_link(page="pages/31_prompting.py", label="Prompting", help="Learning about prompting")

    sac.divider(label="Generating")