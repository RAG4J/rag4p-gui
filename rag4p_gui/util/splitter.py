import tiktoken
from rag4p.indexing.splitters.max_token_splitter import MaxTokenSplitter
from rag4p.indexing.splitters.sentence_splitter import SentenceSplitter
from rag4p.indexing.splitters.single_chunk_splitter import SingleChunkSplitter
from rag4p.integrations.openai import DEFAULT_EMBEDDING_MODEL


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
    else:
        # TODO check if we can add some central logging system or something similar
        raise ValueError(f'Unknown splitter: {splitter_name}')

    return splitter
