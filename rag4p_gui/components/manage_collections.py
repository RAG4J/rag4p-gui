import pandas as pd
import streamlit as st

from rag4p_gui.data.content_store_metadata_service import ContentStoreMetadataService


def create_collection_manager(container, metadata_service: ContentStoreMetadataService, unique_key: str):
    metadata = metadata_service.get_all_meta_data()
    df_collections = pd.DataFrame(metadata)

    with container:
        st.subheader(f"{unique_key} collections")
        my_table = st.dataframe(df_collections, on_select='rerun', selection_mode='multi-row', use_container_width=True)

        if st.button("Delete selected collections", key=f"{unique_key.lower()}_delete_button"):
            for row_index in my_table.selection.rows:
                metadata_service.delete_meta_data(df_collections.loc[row_index, 'collection_name'])
                st.rerun()