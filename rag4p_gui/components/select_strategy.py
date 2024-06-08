import streamlit as st

KEY_SELECTED_STRATEGY = 'selected_strategy'
LKEY_SELECTED_STRATEGY = '_' + KEY_SELECTED_STRATEGY

KEY_WINDOW_SIZE = 'window_size'
LKEY_WINDOW_SIZE = '_' + KEY_WINDOW_SIZE

KEY_AVAILABLE_STRATEGIES = 'available_strategies'


def strategy_available():
    return KEY_SELECTED_STRATEGY in st.session_state


def change_selected_strategy():
    st.session_state[KEY_SELECTED_STRATEGY] = st.session_state.get(LKEY_SELECTED_STRATEGY)
    st.session_state[KEY_WINDOW_SIZE] = st.session_state.get(LKEY_WINDOW_SIZE)


def store_window_size():
    st.session_state[KEY_WINDOW_SIZE] = st.session_state.get(LKEY_WINDOW_SIZE)


def create_retrieval_strategy_selection(container):
    strategies = st.session_state.available_strategies

    if LKEY_SELECTED_STRATEGY in st.session_state:
        index = strategies.index(st.session_state.get(LKEY_SELECTED_STRATEGY))
    elif KEY_SELECTED_STRATEGY in st.session_state:
        index = strategies.index(st.session_state.get(KEY_SELECTED_STRATEGY))
    else:
        index = 0

    with container:
        st.selectbox(label='Choose strategy',
                     options=strategies,
                     key=LKEY_SELECTED_STRATEGY,
                     index=index)

        if st.button('Choose strategy'):
            change_selected_strategy()

        if KEY_WINDOW_SIZE in st.session_state:
            window_value = st.session_state.get(KEY_WINDOW_SIZE)
        else:
            window_value = 1

        st.write('Configure the window size for the window retrieval strategy.')
        st.number_input(label='Window size',
                        min_value=1,
                        key=LKEY_WINDOW_SIZE,
                        on_change=store_window_size,
                        step=1,
                        format='%d',
                        value=window_value,
                        disabled=st.session_state.get(LKEY_SELECTED_STRATEGY) != 'WindowRetrievalStrategy')
