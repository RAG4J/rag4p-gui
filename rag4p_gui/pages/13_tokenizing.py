from itertools import cycle

import streamlit as st
import streamlit_antd_components as sac
import tiktoken
from rag4p.integrations.ollama import PROVIDER as OLLAMA_PROVIDER
from rag4p.integrations.ollama.ollama_tokenizer import tokenizer_for_model
from rag4p.integrations.openai import PROVIDER as OPENAI_PROVIDER
from tokenizers import Tokenizer

from rag4p_gui.indexing_sidebar import IndexingSidebar
from rag4p_gui.my_menu import show_menu_indexing
from rag4p_gui.session import init_session, KEY_SELECTED_EMBEDDER, KEY_SELECTED_EMBEDDING_MODEL

colors = ['magenta', 'red', 'volcano', 'orange', 'gold', 'lime', 'green', 'cyan', 'blue', 'geekblue', 'purple']
color_iter = cycle(colors)


def create_decoder():
    def decode_openai(_token):
        return tokenizer.decode_single_token_bytes(_token).decode('utf-8')

    def decode_ollama(_token):
        return tokenizer.decode([_token])

    provider = st.session_state[KEY_SELECTED_EMBEDDER].lower()

    if provider == OPENAI_PROVIDER:
        decoder = decode_openai
    elif provider == OLLAMA_PROVIDER:
        decoder = decode_ollama
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    return decoder


def pretty_print_tokens(tokens):
    decoder = create_decoder()

    tags = []
    for token in tokens:
        decoded = decoder(token)
        tags.append(sac.Tag(label=f"{token} - {decoded}", color=next(color_iter), closable=False))

    with result_container_tokens:
        sac.tags(tags, align='center')


def pretty_print_matches():
    provider = st.session_state[KEY_SELECTED_EMBEDDER].lower()
    search_string = st.session_state.input_words

    if provider == OPENAI_PROVIDER:
        byte_string = bytes(search_string, 'utf-8')
        matches = [byte.decode('utf-8') for index, byte in enumerate(vocabulary) if byte_string in byte]
    elif provider == OLLAMA_PROVIDER:
        matches = [byte for index, byte in enumerate(vocabulary) if search_string in byte]
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    tags = []
    for match in matches[:10]:
        tags.append(sac.Tag(label=f"{match}", color=next(color_iter), closable=False))

    with pretty_matches_container:
        sac.tags(tags, align='center')


def find_tokenizer():
    provider = st.session_state[KEY_SELECTED_EMBEDDER].lower()
    model = st.session_state[KEY_SELECTED_EMBEDDING_MODEL]

    if provider == OPENAI_PROVIDER:
        encoding = tiktoken.encoding_for_model(model)
    elif provider == OLLAMA_PROVIDER:
        tokenize_model = tokenizer_for_model(model)
        encoding = Tokenizer.from_pretrained(tokenize_model)
    else:
        raise ValueError(f"Unsupported provider: {provider}")
    return encoding


def get_vocabulary():
    provider = st.session_state[KEY_SELECTED_EMBEDDER].lower()

    if provider == OPENAI_PROVIDER:
        return tokenizer.token_byte_values()
    elif provider == OLLAMA_PROVIDER:
        return tokenizer.get_vocab()
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def find_tokens():
    provider = st.session_state[KEY_SELECTED_EMBEDDER].lower()
    text = st.session_state.tokenize_input_text
    if provider == OPENAI_PROVIDER:
        encoded = tokenizer.encode(text)
    elif provider == OLLAMA_PROVIDER:
        encoded = tokenizer.encode(text).ids
    else:
        raise ValueError(f"Unsupported provider: {provider}")
    pretty_print_tokens(encoded)


def find_vocabulary_size():
    provider = st.session_state[KEY_SELECTED_EMBEDDER].lower()

    if provider == OPENAI_PROVIDER:
        return tokenizer.n_vocab
    elif provider == OLLAMA_PROVIDER:
        return len(tokenizer.get_vocab())
    else:
        raise ValueError(f"Unsupported provider: {provider}")


st.set_page_config(page_title='RAG4P GUI ~ Tokenization', page_icon='🔪', layout='wide')

init_session()

sidebar = IndexingSidebar(embeddings=st.session_state.available_embedders)
sidebar.add_sidebar()

show_menu_indexing()

st.write("## Tokenization")
with st.expander("See explanation"):
    st.markdown("""
    Models work with numbers, not text. To convert text into numbers, we need to tokenize the text. In Lexical search we 
    are used to tokenizers like WhitespaceTokenizer or CharTokenizer. When working with embeddings, a tokenizer works a bit
    differently. It is used to split the text into tokens, which are then converted into numbers. THe only thing is, there 
    is a limited set of tokens. These are available in the vocabulary of the tokenizer. If a token is not in the vocabulary,
    it is broken down into sub-tokens. The final sub-token is a character. Each token is a number in the dictionary.
    
    cl100k_base is the dictionary used by the recent models of OpenAI like GPT-4.
    o200k_base is the dictionary used by the most recent model of OpenAI like GPT-4o.
    """)

tokenizer = find_tokenizer()
vocabulary = get_vocabulary()

st.write(f"Chosen vocabulary size: {find_vocabulary_size()}")

input_text = st.text_area(label='Enter text to tokenize',
                          height=100,
                          key='tokenize_input_text',
                          on_change=find_tokens)
result_container_tokens = st.container()

st.text_input(label='Find tokens containing what you type', on_change=pretty_print_matches, key='input_words')
pretty_matches_container = st.container()
