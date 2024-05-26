import tiktoken
from rag4p.indexing.splitters.max_token_splitter import MaxTokenSplitter
from rag4p.indexing.splitters.sentence_splitter import SentenceSplitter
from rag4p.indexing.splitters.single_chunk_splitter import SingleChunkSplitter
from rag4p.integrations.openai import DEFAULT_EMBEDDING_MODEL


def create_splitter(splitter_name: str, embedding_model: str, chunk_size: int):
    if splitter_name == 'sentence':
        message = '#### Chunking by _sentence_'
        splitter = SentenceSplitter()
    elif splitter_name == 'max size':
        message = f'#### Chunking by _max size_ ({chunk_size} tokens)'
        try:
            model = embedding_model
            tiktoken.encoding_for_model(model_name=model)
        except KeyError as e:
            model = DEFAULT_EMBEDDING_MODEL  # only supported for OpenAI models
            message = (f'The selected model _{embedding_model}_ is not '
                       f'available. Using default model _{model}_.')
        splitter = MaxTokenSplitter(max_tokens=chunk_size, model=model)
    elif splitter_name == 'single chunk':
        message = '#### Single chunk'
        splitter = SingleChunkSplitter()
    else:
        message = 'Unknown splitter'
        splitter = None

    return message, splitter
