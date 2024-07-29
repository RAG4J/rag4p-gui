import streamlit as st
from rag4p_gui.footer import footer
from rag4p_gui.my_menu import show_menu
from rag4p_gui.session import init_session


st.set_page_config(page_title='RAG4P GUI', page_icon='🧠', layout='wide')


init_session()

show_menu()

# Define custom CSS for styling links
custom_css = """
<style>
a {
    font-family: 'Courier New', Courier, monospace;
    color: #4A90E2; /* Change the color */
    text-decoration: none; /* Remove underline */
    font-weight: bolder; /* Make it bold */
}

a:hover {
    color: #F56A00; /* Change color on hover */
    text-decoration: underline; /* Add underline on hover */
}
</style>
"""

# Inject custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

st.title('RAG4P Experimental GUI')
st.markdown(
    f"""
    This is an experimental GUI for the RAG4P project. You can use this GUI to interact with the RAG4P API. 
    You can configure the embedding model to use in the sidebar.    
    """
)
col1, col2 = st.columns(2)
with col1:
    col11, col12 = st.columns([1, 2])
    with col11:
        st.image(image='https://rag4j.org/assets/images/jettro-coenradie.jpg', caption='Jettro Coenradie', width=200)
    with col12:
        st.markdown("""
### LinkedIn
[https://www.linkedin.com/in/jettro](https://www.linkedin.com/in/jettro)
### Blog
[https://jettro.dev](https://jettro.dev)
### Luminis  
[https://luminis.eu](https://luminis.eu)
""")


with col2:
    col21, col22 = st.columns([1, 2])
    with col21:
        st.image(image='https://rag4j.org/assets/images/rag4j-logo.png', caption='RAG4P Logo', width=200)
    with col22:
        st.write("We developed this project to learn and to teach. We have a lot of experience with search-based "
                 "systems. With the power of Large Language Models and Retrieval Augmented Generation, we see a lot of "
                 "possibilities to improve search-based systems. We started using many Python frameworks and the Java "
                 "Langchain4j project. We wanted to create something focused on RAG that is easy to use and extend. We "
                 "wanted to have RAG quality integrated into the framework. In the TruLens project, we found "
                 "inspiration to embed a quality metric using Large Language Models. We tried to keep it as simple as "
                 "possible to use. Head to the documentation page to learn more about the framework.")
        st.markdown("[https://rag4p.org](https://rag4p.org)")

footer()