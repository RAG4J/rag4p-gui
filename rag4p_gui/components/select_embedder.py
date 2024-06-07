import streamlit as st

KEY_SELECTED_EMBEDDER = 'selected_embedder'
LKEY_SELECTED_EMBEDDER = '_' + KEY_SELECTED_EMBEDDER
KEY_SELECTED_EMBEDDING_MODEL = 'selected_embedding_model'
LKEY_SELECTED_EMBEDDING_MODEL = '_' + KEY_SELECTED_EMBEDDING_MODEL
KEY_AVAILABLE_EMBEDDERS = 'available_embedders'


def store_selected_model():
    st.session_state[KEY_SELECTED_EMBEDDING_MODEL] = st.session_state.get(LKEY_SELECTED_EMBEDDING_MODEL)


def store_selected_embedder():
    embeddings = st.session_state[KEY_AVAILABLE_EMBEDDERS]

    st.session_state[KEY_SELECTED_EMBEDDER] = st.session_state.get(LKEY_SELECTED_EMBEDDER)
    # Update the selected model to use the first model from the selected embedder
    st.session_state[KEY_SELECTED_EMBEDDING_MODEL] = \
        embeddings.loc[embeddings['embedder'] == st.session_state.selected_embedder, 'model'].values[0][0]


def create_embedder_selector(container):
    embeddings = st.session_state[KEY_AVAILABLE_EMBEDDERS]

    if LKEY_SELECTED_EMBEDDER not in st.session_state:
        if KEY_SELECTED_EMBEDDER in st.session_state:
            st.session_state[LKEY_SELECTED_EMBEDDER] = st.session_state.get(KEY_SELECTED_EMBEDDER)
        else:
            st.session_state[LKEY_SELECTED_EMBEDDER] = embeddings['embedder'].values[0]

        if KEY_SELECTED_EMBEDDING_MODEL in st.session_state:
            st.session_state[LKEY_SELECTED_EMBEDDING_MODEL] = st.session_state.get(KEY_SELECTED_EMBEDDING_MODEL)
        else:
            st.session_state[LKEY_SELECTED_EMBEDDING_MODEL] = \
                embeddings.loc[embeddings['embedder'] == st.session_state[LKEY_SELECTED_EMBEDDER], 'model'].values[0][0]

    with container:
        st.write('Configure the embedding to use. First you choose the provider and then the model.')
        st.selectbox(label='Choose provider',
                     options=embeddings['embedder'].tolist(),
                     key=LKEY_SELECTED_EMBEDDER,
                     on_change=store_selected_embedder)
        selected_embedder = st.session_state.get(LKEY_SELECTED_EMBEDDER)
        model_options = embeddings.loc[embeddings['embedder'] == selected_embedder, 'model'].values[0]
        st.selectbox(label='Choose model',
                     options=model_options,
                     key=LKEY_SELECTED_EMBEDDING_MODEL,
                     on_change=store_selected_model)
