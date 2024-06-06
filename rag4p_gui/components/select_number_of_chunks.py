import streamlit as st

from rag4p_gui.components.select_retriever import KEY_CHOSEN_RETRIEVER

KEY_AMOUNT_OF_CHUNKS = 'amount_of_chunks'
LKEY_AMOUNT_OF_CHUNKS = '_' + KEY_AMOUNT_OF_CHUNKS


def store_amount_of_chunks():
    st.session_state[KEY_AMOUNT_OF_CHUNKS] = st.session_state.get(LKEY_AMOUNT_OF_CHUNKS)


def create_number_of_chunks_selection(chunks_container):

    if KEY_CHOSEN_RETRIEVER in st.session_state:
        if LKEY_AMOUNT_OF_CHUNKS in st.session_state:
            amount_of_chunks_value = st.session_state.get(LKEY_AMOUNT_OF_CHUNKS)
        elif KEY_AMOUNT_OF_CHUNKS in st.session_state:
            amount_of_chunks_value = st.session_state.get(KEY_AMOUNT_OF_CHUNKS)
        else:
            amount_of_chunks_value = 1

        with chunks_container:
            st.write('Configure the amount of chunks to return.')
            st.number_input(label='Amount of chunks',
                            min_value=1,
                            key=LKEY_AMOUNT_OF_CHUNKS,
                            on_change=store_amount_of_chunks,
                            step=1,
                            format='%d',
                            value=amount_of_chunks_value)


