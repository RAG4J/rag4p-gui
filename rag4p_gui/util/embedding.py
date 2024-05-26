from rag4p.integrations.ollama.access_ollama import AccessOllama
from rag4p.integrations.ollama.ollama_embedder import OllamaEmbedder
from rag4p.integrations.openai.openai_embedder import OpenAIEmbedder
from rag4p.rag.embedding.local.onnx_embedder import OnnxEmbedder
from rag4p.util.key_loader import KeyLoader


def create_embedder(embedder_name: str, model_name: str):
    key_loader = KeyLoader()

    if embedder_name == 'OpenAI':
        embedder = OpenAIEmbedder(api_key=key_loader.get_openai_api_key(), embedding_model=model_name)
    elif embedder_name == 'Ollama':
        access_ollama = AccessOllama()
        embedder = OllamaEmbedder(access_ollama=access_ollama, model=model_name)
    elif embedder_name == 'Local':
        embedder = OnnxEmbedder()
    else:
        raise ValueError('Unknown embedder')

    return embedder
