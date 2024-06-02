import streamlit as st
import streamlit_antd_components as sac


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
                if key not in ['create_date', 'supplier', 'model', 'splitter', 'embedder', 'name']:
                    st.markdown(f"*{key}*: **{metadata[key]}**")

    else:
        st_container.info('No content found, while it should be there.')
