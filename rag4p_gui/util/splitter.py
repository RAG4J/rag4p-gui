import tiktoken
from dotenv import load_dotenv

from rag4p.indexing.splitters.max_token_splitter import MaxTokenSplitter
from rag4p.indexing.splitters.sentence_splitter import SentenceSplitter
from rag4p.indexing.splitters.single_chunk_splitter import SingleChunkSplitter
from rag4p.indexing.splitters.section_splitter import SectionSplitter
from rag4p.indexing.splitters.semantic_splitter import SemanticSplitter
from rag4p.indexing.splitter_chain import SplitterChain
from rag4p.integrations.openai import DEFAULT_EMBEDDING_MODEL
from rag4p.integrations.openai.openai_knowledge_extractor import OpenaiKnowledgeExtractor
from rag4p.integrations.ollama.access_ollama import AccessOllama
from rag4p.integrations.ollama.ollama_knowledge_extractor import OllamaKnowledgeExtractor
from rag4p.util.key_loader import KeyLoader

from rag4p_gui.util import SECTION_SEMANTIC_OLLAMA_SPLITTER, SECTION_SEMANTIC_OPENAI_SPLITTER

load_dotenv()
key_loader = KeyLoader()


def create_splitter(splitter_name: str, **kwargs):
    """
    Create a splitter based on the provided name. Some splitters require additional arguments. Or defaults are used.
    sentence: Split the content into sentences.
    max size: Split the content into chunks of a maximum size. Additional parameters are: chunk_size, embedding_model
    single chunk: Do not split the content.
    :param splitter_name:
    :param kwargs: Optional arguments to pass to the splitter.
    :return:
    """
    if splitter_name == SentenceSplitter.name():
        splitter = SentenceSplitter()
    elif splitter_name == MaxTokenSplitter.name():
        chunk_size = kwargs.get('chunk_size', 512)
        model = kwargs.get('embedding_model')
        provider = kwargs.get('provider')
        splitter = MaxTokenSplitter(max_tokens=chunk_size, provider=provider, model=model)
    elif splitter_name == SingleChunkSplitter.name():
        splitter = SingleChunkSplitter()
    elif splitter_name == SectionSplitter.name():
        splitter = SectionSplitter()
    elif splitter_name == SemanticSplitter.name():
        openai_api_key = key_loader.get_openai_api_key()
        knowledge_extractor = OpenaiKnowledgeExtractor(openai_api_key=openai_api_key)
        splitter = SplitterChain([SectionSplitter(), SemanticSplitter(knowledge_extractor=knowledge_extractor)])
    elif splitter_name == SECTION_SEMANTIC_OLLAMA_SPLITTER:
        assess_ollama = AccessOllama()
        knowledge_extractor = OllamaKnowledgeExtractor(access_ollama=assess_ollama)
        splitter = SplitterChain([SectionSplitter(), SemanticSplitter(knowledge_extractor=knowledge_extractor)])
    elif splitter_name == SECTION_SEMANTIC_OPENAI_SPLITTER:
        openai_api_key = key_loader.get_openai_api_key()
        knowledge_extractor = OpenaiKnowledgeExtractor(openai_api_key=openai_api_key)
        splitter = SplitterChain([SectionSplitter(), SemanticSplitter(knowledge_extractor=knowledge_extractor)])
    else:
        # TODO check if we can add some central logging system or something similar
        raise ValueError(f'Unknown splitter: {splitter_name}')

    return splitter
