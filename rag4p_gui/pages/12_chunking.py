import streamlit as st
from rag4p.indexing.input_document import InputDocument

from rag4p_gui.components.select_splitter import KEY_SELECTED_SPLITTER, KEY_CHUNK_SIZE
from rag4p_gui.indexing_sidebar import add_indexing_sidebar
from rag4p_gui.my_menu import show_menu_indexing
from rag4p_gui.session import init_session, KEY_SELECTED_EMBEDDING_MODEL, KEY_SELECTED_EMBEDDER
from rag4p_gui.util.splitter import create_splitter


def chunk_document():
    splitter = create_splitter(splitter_name=st.session_state[KEY_SELECTED_SPLITTER],
                               provider=st.session_state[KEY_SELECTED_EMBEDDER].lower(),
                               embedding_model=st.session_state[KEY_SELECTED_EMBEDDING_MODEL],
                               chunk_size=st.session_state[KEY_CHUNK_SIZE])

    chunks = splitter.split(input_document=InputDocument(document_id='1',
                                                         text=st.session_state.get('input_document'),
                                                         properties={}))
    for chunk in chunks:
        chunk_text = chunk.chunk_text.replace("\n", " ")
        result_container.write(f'{chunk.chunk_id}. {chunk_text}')


st.set_page_config(page_title='RAG4P GUI ~ Chunking', page_icon='🔪', layout='wide')
init_session()

add_indexing_sidebar()
show_menu_indexing()

st.write("## Chunking")

st.text_area(label='Input document', height=200, key='input_document')

splitter_name = st.session_state.selected_splitter

result_container = st.container()

if st.session_state.get('input_document') is not None:
    chunk_document()
