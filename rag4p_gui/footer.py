import streamlit as st


def footer():
    footer_html = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: black;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
      <p>Developed by <a href="https://www.linkedin.com/in/jettro" target="_blank">Jettro Coenradie</a>. Visit <a href="https://jettro.dev" target="_blank">jettro.dev</a> for more projects.<img src="https://rag4j.org/assets/images/luminis.png" alt="Luminis Logo" height="40"></p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)
