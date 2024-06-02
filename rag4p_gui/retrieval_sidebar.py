import streamlit as st

from rag4p.rag.retrieval.strategies.document_retrieval_strategy import DocumentRetrievalStrategy
from rag4p.rag.retrieval.strategies.topn_retrieval_strategy import TopNRetrievalStrategy
from rag4p.rag.retrieval.strategies.window_retrieval_strategy import WindowRetrievalStrategy

from rag4p_gui.session import KEY_SELECTED_STRATEGY, KEY_WINDOW_SIZE

LKEY_SELECTED_STRATEGY = '_' + KEY_SELECTED_STRATEGY
LKEY_WINDOW_SIZE = '_' + KEY_WINDOW_SIZE
KEY_RETRIEVAL_STRATEGY = 'retrieval_strategy'


class RetrievalSidebar:
    def __init__(self):
        st.session_state[LKEY_SELECTED_STRATEGY] = st.session_state[KEY_SELECTED_STRATEGY]
        st.session_state[LKEY_WINDOW_SIZE] = st.session_state[KEY_WINDOW_SIZE]
        self._create_strategy()

    @staticmethod
    def store_selected_strategy():
        st.session_state[KEY_SELECTED_STRATEGY] = st.session_state.get(LKEY_SELECTED_STRATEGY)

    @staticmethod
    def store_window_size():
        st.session_state[KEY_WINDOW_SIZE] = st.session_state.get(LKEY_WINDOW_SIZE)

    @staticmethod
    def _create_strategy():
        content_store = st.session_state.content_store
        if st.session_state[KEY_SELECTED_STRATEGY] == TopNRetrievalStrategy.__name__:
            strategy = TopNRetrievalStrategy(retriever=content_store)
        elif st.session_state[KEY_SELECTED_STRATEGY] == WindowRetrievalStrategy.__name__:
            window_size = st.session_state[KEY_WINDOW_SIZE]
            strategy = WindowRetrievalStrategy(retriever=content_store, window_size=window_size)
        elif st.session_state[KEY_SELECTED_STRATEGY] == DocumentRetrievalStrategy.__name__:
            strategy = DocumentRetrievalStrategy(retriever=content_store)
        else:
            raise ValueError(f"Unsupported retrieval strategy: {st.session_state.selected_retrieval_strategy}")
        st.session_state[KEY_RETRIEVAL_STRATEGY] = strategy

    def add_sidebar(self):
        with st.sidebar:
            st.title('Configure')
            with st.container(border=True):
                st.write('Configure the retrieval strategy to use.')
                st.selectbox(label='Choose strategy',
                             options=st.session_state.available_strategies,
                             key=LKEY_SELECTED_STRATEGY,
                             on_change=self.store_selected_strategy)

            with st.container(border=True):
                st.write('Configure the window size for the window retrieval strategy.')
                st.number_input(label='Window size',
                                min_value=1,
                                key=LKEY_WINDOW_SIZE,
                                on_change=self.store_window_size,
                                step=1,
                                format='%d',
                                disabled=st.session_state.get(LKEY_SELECTED_STRATEGY) != 'WindowRetrievalStrategy')
