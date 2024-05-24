import streamlit as st
import tiktoken
from rag4p.indexing.input_document import InputDocument
from rag4p.indexing.splitters.max_token_splitter import MaxTokenSplitter
from rag4p.indexing.splitters.sentence_splitter import SentenceSplitter
from rag4p.indexing.splitters.single_chunk_splitter import SingleChunkSplitter
from rag4p.integrations.openai import DEFAULT_EMBEDDING_MODEL

from rag4p_gui.my_menu import show_menu
from rag4p_gui.my_sidebar import MySidebar
from rag4p_gui.session import init_session


def chunk_document():
    if splitter_name == 'sentence':
        result_container.markdown('#### Chunking by _sentence_')
        splitter = SentenceSplitter()
    elif splitter_name == 'max size':
        result_container.markdown(f'#### Chunking by _max size_ ({st.session_state.chunk_size} tokens)')
        try:
            model = st.session_state.selected_embedding_model
            tiktoken.encoding_for_model(model_name=model)
        except KeyError as e:
            model = DEFAULT_EMBEDDING_MODEL
            result_container.info(f'The selected model _{st.session_state.selected_embedding_model}_ is not '
                                      f'available. Using default model _{model}_.')
        splitter = MaxTokenSplitter(max_tokens=st.session_state.chunk_size, model=model)
    elif splitter_name == 'single chunk':
        result_container.markdown('#### Single chunk')
        splitter = SingleChunkSplitter()
    else:
        result_container.write('Unknown splitter')
        return

    chunks = splitter.split(input_document=InputDocument(document_id='1',
                                                         text=st.session_state.get('input_document'),
                                                         properties={}))
    for chunk in chunks:
        chunk_text = chunk.chunk_text.replace("\n", " ")
        result_container.write(f'{chunk.chunk_id}. {chunk_text}')


st.set_page_config(page_title='RAG4P GUI ~ Chunking', page_icon='🔪', layout='wide')
init_session()

sidebar = MySidebar(embeddings=st.session_state.available_embedders)
sidebar.add_sidebar()
show_menu()

st.write("## Chunking")

st.text_area(label='Input document', height=200, key='input_document')

splitter_name = st.session_state.selected_splitter

result_container = st.container()

if st.session_state.get('input_document') is not None:
    chunk_document()
