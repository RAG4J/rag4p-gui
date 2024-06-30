import streamlit as st
from openai import OpenAI
from rag4p.integrations.bedrock.access_bedrock import AccessBedrock
from rag4p.integrations.bedrock.bedrock_answer_generator import BedrockAnswerGenerator
from rag4p.integrations.ollama.access_ollama import AccessOllama
from rag4p.integrations.ollama.ollama_answer_generator import OllamaAnswerGenerator
from rag4p.integrations.openai.openai_answer_generator import OpenaiAnswerGenerator
from rag4p.util.key_loader import KeyLoader

from rag4p_gui.components.select_llm import KEY_SELECTED_LLM_PROVIDER, KEY_SELECTED_LLM_MODEL


def construct_answer(answer_context: str, question: str, key_loader: KeyLoader = KeyLoader()):
    if KEY_SELECTED_LLM_PROVIDER not in st.session_state or KEY_SELECTED_LLM_MODEL not in st.session_state:
        st.error("No LLM provider or model selected")
        return

    model_ = st.session_state[KEY_SELECTED_LLM_MODEL]
    if st.session_state[KEY_SELECTED_LLM_PROVIDER].lower() == 'ollama':
        access_ollama = AccessOllama()
        answer_generator = OllamaAnswerGenerator(access_ollama=access_ollama, model=model_)
    elif st.session_state[KEY_SELECTED_LLM_PROVIDER].lower() == 'openai':
        answer_generator = OpenaiAnswerGenerator(openai_api_key=key_loader.get_openai_api_key(), openai_model=model_)
    elif st.session_state[KEY_SELECTED_LLM_PROVIDER].lower() == 'bedrock':
        access_bedrock = AccessBedrock(region_name=key_loader.get_bedrock_region(),
                                       profile_name=key_loader.get_bedrock_profile())
        answer_generator = BedrockAnswerGenerator(model=model_, access_bedrock=access_bedrock)
    else:
        st.error("No LLM provider selected")
        return

    return answer_generator.generate_answer(question=question, context=answer_context)


def chat_answer(prompt: str, key_loader: KeyLoader = KeyLoader()):
    if KEY_SELECTED_LLM_PROVIDER not in st.session_state or KEY_SELECTED_LLM_MODEL not in st.session_state:
        st.error("No LLM provider or model selected")
        return

    model_ = st.session_state[KEY_SELECTED_LLM_MODEL]
    if st.session_state[KEY_SELECTED_LLM_PROVIDER].lower() == 'ollama':
        access_ollama = AccessOllama()
        prompt_ = f"You are a helpfull assistant. {prompt}"
        answer = access_ollama.generate_answer(prompt=prompt, model=model_)
    elif st.session_state[KEY_SELECTED_LLM_PROVIDER].lower() == 'openai':
        openai_client = OpenAI(api_key=key_loader.get_openai_api_key())

        completion = openai_client.chat.completions.create(
            model=model_,
            messages=[
                {"role": "system", "content": "You are a helpfull assistant."},
                {"role": "user", "content": prompt},
            ],
            stream=False,
        )

        answer = completion.choices[0].message.content

    elif st.session_state[KEY_SELECTED_LLM_PROVIDER].lower() == 'bedrock':
        access_bedrock = AccessBedrock(region_name=key_loader.get_bedrock_region(),
                                       profile_name=key_loader.get_bedrock_profile())
        prompt_ = f"You are a helpfull assistant. {prompt}"
        answer = access_bedrock.generate_answer(prompt=prompt_, model=model_)
    else:
        st.error("No LLM provider selected")
        return

    return answer
