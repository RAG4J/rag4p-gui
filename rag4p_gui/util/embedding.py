from rag4p.integrations.ollama.access_ollama import AccessOllama
from rag4p.integrations.ollama.ollama_embedder import OllamaEmbedder
from rag4p.integrations.openai.openai_embedder import OpenAIEmbedder
from rag4p.integrations.bedrock.bedrock_embedder import BedrockEmbedder
from rag4p.integrations.bedrock.access_bedrock import AccessBedrock
from rag4p.util.key_loader import KeyLoader


def create_embedder(embedder_name: str, model_name: str):
    key_loader = KeyLoader()

    if embedder_name == OpenAIEmbedder.supplier():
        embedder = OpenAIEmbedder(api_key=key_loader.get_openai_api_key(), embedding_model=model_name)
    elif embedder_name == OllamaEmbedder.supplier():
        access_ollama = AccessOllama()
        embedder = OllamaEmbedder(access_ollama=access_ollama, model=model_name)
    elif embedder_name == BedrockEmbedder.supplier():
        access_bedrock = AccessBedrock.init_from_env(key_loader=key_loader)
        embedder = BedrockEmbedder(access_bedrock=access_bedrock, model=model_name)
    else:
        # TODO check if we can add some central logging system or something similar
        raise ValueError(f'Unknown embedder: {embedder_name}')

    return embedder
