from itertools import cycle

import streamlit as st
import tiktoken
import streamlit_antd_components as sac

from rag4p_gui.my_menu import show_menu, show_menu_indexing
from rag4p_gui.my_sidebar import MySidebar
from rag4p_gui.session import init_session


def pretty_print_tokens(tokens):
    colors = ['magenta', 'red', 'volcano', 'orange', 'gold', 'lime', 'green', 'cyan', 'blue', 'geekblue', 'purple']
    color_iter = cycle(colors)

    tags = []
    for token in tokens:
        decoded = tokenizer.decode_single_token_bytes(token).decode('utf-8')
        tags.append(sac.Tag(label=f"{token} - {decoded}", color=next(color_iter), closable=False))

    sac.tags(tags, align='center')


def pretty_print_matches():
    search_string = st.session_state.input_words
    byte_string = bytes(search_string, 'utf-8')
    exact_matches = [byte_string] if byte_string in vocabulary else []
    matches = [byte for index, byte in enumerate(vocabulary) if byte_string in byte]
    all_matches = exact_matches + matches

    colors = ['magenta', 'red', 'volcano', 'orange', 'gold', 'lime', 'green', 'cyan', 'blue', 'geekblue', 'purple']
    color_iter = cycle(colors)

    tags = []
    for byte in all_matches[:10]:
        tags.append(sac.Tag(label=f"{byte.decode('utf-8')}", color=next(color_iter), closable=False))

    with pretty_matches_container:
        sac.tags(tags, align='center')


st.set_page_config(page_title='RAG4P GUI ~ Tokenization', page_icon='🔪', layout='wide')

init_session()

sidebar = MySidebar(embeddings=st.session_state.available_embedders)
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

encoding_names = tiktoken.list_encoding_names()

selected_encoding = st.selectbox(label='Choose encoding',
                                 options=encoding_names,
                                 index=encoding_names.index('o200k_base'))
tokenizer = tiktoken.get_encoding(selected_encoding)
vocabulary = tokenizer.token_byte_values()

st.write(f"Chosen vocabulary size: {tokenizer.n_vocab}")

input_text = st.text_area(label='Enter text to tokenize', height=100)
encoded = tokenizer.encode(input_text)
pretty_print_tokens(encoded)

st.text_input(label='Find tokens containing what you type', on_change=pretty_print_matches, key='input_words')
pretty_matches_container = st.container()
