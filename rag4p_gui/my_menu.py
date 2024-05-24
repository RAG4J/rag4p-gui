import streamlit as st


def show_menu():
    page1, page2, page3, page4, page5, page6 = st.columns(6, gap="small")
    with page1:
        st.page_link(page="home.py", label="Home", icon="🏠", help="Go back to the home page")
    with page2:
        st.page_link(page="pages/1_embeddings.py", label="Embeddings", icon="🧠", help="Learn about embeddings")
    with page3:
        st.page_link(page="pages/2_chunking.py", label="Chunking", icon="🔪", help="Learn about chunking")
    with page4:
        st.page_link(page="pages/3_tokenization.py", label="Tokenization", icon="🔪", help="Learn about tokenization")
