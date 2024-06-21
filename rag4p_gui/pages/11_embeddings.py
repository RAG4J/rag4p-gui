import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from sklearn.manifold import TSNE

from rag4p_gui.components.select_content_store import create_content_store_selection
from rag4p_gui.components.select_embedder import KEY_SELECTED_EMBEDDER, KEY_SELECTED_EMBEDDING_MODEL
from rag4p_gui.containers import info_content_store
from rag4p_gui.indexing_sidebar import add_indexing_sidebar
from rag4p_gui.my_menu import show_menu_indexing
from rag4p_gui.session import init_session
from rag4p_gui.util.embedding import create_embedder

load_dotenv()


def embed_document():
    try:
        embedder = create_embedder(embedder_name=st.session_state.selected_embedder,
                                   model_name=st.session_state.selected_embedding_model)
    except ValueError:
        result_container.write('Unknown embedder')
        return

    text_to_embed = st.session_state.get('text_to_embed')
    embedding = embedder.embed(text=text_to_embed)
    result_container.write(f'Length of Embedding: {len(embedding)}')


def compute_embeddings(algorithm_params_, data_frame):
    features = np.array(data_frame["embedding"].tolist())

    tsne = TSNE(
        n_components=2,
        perplexity=algorithm_params_["perplexity"],
        random_state=algorithm_params_["random_state"],
        max_iter=algorithm_params_["n_iter"],
        learning_rate=algorithm_params_["learning_rate"],
        n_iter_without_progress=algorithm_params_["n_iter_without_progress"],
    )
    proj_2d_ = tsne.fit_transform(
        features,
    )

    proj_2d_ = pd.concat([data_frame, pd.DataFrame(proj_2d_)], axis=1)

    return proj_2d_


st.set_page_config(page_title='RAG4P GUI ~ Embeddings', page_icon='🧠', layout='wide')
init_session()

add_indexing_sidebar()
show_menu_indexing()

st.write("## Embeddings")

chosen_embedder = st.session_state[KEY_SELECTED_EMBEDDER]
chosen_model = st.session_state[KEY_SELECTED_EMBEDDING_MODEL]

st.text_input(label='Text to embed', key='text_to_embed')

result_container = st.container()

if st.session_state.get('text_to_embed') is not None and len(st.session_state.get('text_to_embed')) > 0:
    embed_document()

content_store = st.session_state.content_store
vector_store = content_store.vector_store
vector_size = len(vector_store.iloc[0]["embedding"])

algorithm_params = {
    "perplexity": 30,
    "random_state": 25,
    "learning_rate": 0.1,
    "n_iter": 1000,
    "n_iter_without_progress": 300,
    "dimensions": vector_size,
}

proj_2d = compute_embeddings(algorithm_params, vector_store)

fig_2d = px.scatter(
    proj_2d,
    x=0,
    y=1,
    hover_data=["chunk_id"],
    color=None,
)

st.subheader("Embeddings for current content store")
create_content_store_selection()
expander = st.expander("Show content store details")
info_content_store(expander)
with st.container():
    st.plotly_chart(fig_2d, theme="streamlit", use_container_width=True)
