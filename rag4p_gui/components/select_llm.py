import streamlit as st

KEY_SELECTED_LLM_PROVIDER = 'selected_llm_provider'
LKEY_SELECTED_LLM_PROVIDER = '_' + KEY_SELECTED_LLM_PROVIDER
KEY_SELECTED_LLM_MODEL = 'selected_llm_model'
LKEY_SELECTED_LLM_MODEL = '_' + KEY_SELECTED_LLM_MODEL
KEY_AVAILABLE_LLMS = 'available_llms'


def store_selected_model():
    st.session_state[KEY_SELECTED_LLM_MODEL] = st.session_state.get(LKEY_SELECTED_LLM_MODEL)


def store_selected_llm():
    llms = st.session_state[KEY_AVAILABLE_LLMS]

    st.session_state[KEY_SELECTED_LLM_PROVIDER] = st.session_state.get(LKEY_SELECTED_LLM_PROVIDER)
    # Update the selected model to use the first model from the selected llm
    st.session_state[KEY_SELECTED_LLM_MODEL] = \
        llms.loc[llms['llm'] == st.session_state.selected_llm_provider, 'model'].values[0][0]


def create_llm_selection(container):
    llms = st.session_state[KEY_AVAILABLE_LLMS]

    if LKEY_SELECTED_LLM_PROVIDER not in st.session_state:
        index_llm = llms['llm'].tolist().index(st.session_state.get(KEY_SELECTED_LLM_PROVIDER))
        models = llms.loc[llms['llm'] == st.session_state[KEY_SELECTED_LLM_PROVIDER], 'model'].values[0]
        index_model = models.index(st.session_state.get(KEY_SELECTED_LLM_MODEL))
    else:
        index_llm = llms['llm'].tolist().index(st.session_state.get(LKEY_SELECTED_LLM_PROVIDER))
        models = llms.loc[llms['llm'] == st.session_state[LKEY_SELECTED_LLM_PROVIDER], 'model'].values[0]
        if LKEY_SELECTED_LLM_MODEL in models:
            index_model = models.index(st.session_state.get(KEY_SELECTED_LLM_MODEL))
        else:
            index_model = 0

    with container:
        st.write('Configure the LLM to use. First you choose the provider and then the model.')
        st.selectbox(label='Choose provider',
                     options=llms['llm'].tolist(),
                     key=LKEY_SELECTED_LLM_PROVIDER,
                     index=index_llm)
        selected_llm = st.session_state.get(LKEY_SELECTED_LLM_PROVIDER)
        model_options = llms.loc[llms['llm'] == selected_llm, 'model'].values[0]
        st.selectbox(label='Choose model',
                     options=model_options,
                     key=LKEY_SELECTED_LLM_MODEL,
                     index=index_model)

        if st.button('Choose LLM'):
            store_selected_llm()
            store_selected_model()