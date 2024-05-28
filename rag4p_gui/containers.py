import streamlit as st


def info_content_store(st_container):
    if 'content_store' in st.session_state and st.session_state.content_store is not None:
        num_chunks = 0
        for chunk in st.session_state.content_store.loop_over_chunks():
            num_chunks += 1
        metadata = st.session_state.content_store.get_metadata()
        st_container.markdown(
            f"""
            *Number of chunks*: **{num_chunks}**

            *Embedder*: **{metadata["supplier"]}**

            *Embedding model*: **{metadata["model"]}**
        """)
    else:
        st_container.info('No content found, while it should be there.')
