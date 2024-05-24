import streamlit as st
from rag4p.indexing.input_document import InputDocument
from rag4p.indexing.splitters.max_token_splitter import MaxTokenSplitter
from rag4p.indexing.splitters.sentence_splitter import SentenceSplitter
from rag4p.indexing.splitters.single_chunk_splitter import SingleChunkSplitter

from rag4p_gui.my_menu import show_menu
from rag4p_gui.my_sidebar import MySidebar
from rag4p_gui.session import init_session


def chunk_document():
    if st.session_state.selected_splitter == 'sentence':
        result_container.write('Chunking by sentence')
        splitter = SentenceSplitter()
    elif st.session_state.selected_splitter == 'max size':
        result_container.write('Chunking by max size')
        splitter = MaxTokenSplitter(max_tokens=st.session_state.chunk_size)
    elif st.session_state.selected_splitter == 'single chunk':
        result_container.write('Single chunk')
        splitter = SingleChunkSplitter()
    else:
        result_container.write('Unknown splitter')
        pass

    chunks = splitter.split(input_document=InputDocument(document_id='1', text=input_document, properties={}))
    for chunk in chunks:
        chunk_text = chunk.chunk_text.replace("\n", " ")
        result_container.write(f'{chunk.chunk_id}. {chunk_text}')


st.set_page_config(page_title='RAG4P GUI ~ Chunking', page_icon='🔪', layout='wide')
init_session()

sidebar = MySidebar(embeddings=st.session_state.available_embedders)
sidebar.add_sidebar()
show_menu()

st.write("## Chunking")

input_document = st.text_area(label='Input document', height=200)

st.button('Chunk document', on_click=chunk_document)

result_container = st.container()
